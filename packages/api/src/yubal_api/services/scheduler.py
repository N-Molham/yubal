"""Background scheduler for periodic subscription syncing."""

import asyncio
import logging
from datetime import UTC, datetime
from uuid import UUID

from croniter import croniter

from yubal_api.api.exceptions import SubscriptionNotFoundError
from yubal_api.db.subscription import Subscription, SubscriptionOrigin
from yubal_api.domain.enums import JobSource
from yubal_api.services.job_executor import JobExecutor
from yubal_api.services.library_sync_service import LibrarySyncService
from yubal_api.services.runtime_settings import RuntimeSettingsService
from yubal_api.services.subscription_service import SubscriptionService
from yubal_api.settings import Settings

logger = logging.getLogger(__name__)


class Scheduler:
    """Background scheduler that syncs enabled subscriptions periodically."""

    def __init__(
        self,
        subscription_service: SubscriptionService,
        job_executor: JobExecutor,
        settings: Settings,
        *,
        library_sync: LibrarySyncService,
        runtime_settings: RuntimeSettingsService,
    ) -> None:
        """Initialize scheduler."""
        self._subscription_service = subscription_service
        self._job_executor = job_executor
        self._settings = settings
        self._library_sync = library_sync
        self._runtime_settings = runtime_settings
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()
        self._wake_event = asyncio.Event()
        self._next_run_at: datetime | None = None

    @property
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._task is not None and not self._task.done()

    @property
    def enabled(self) -> bool:
        """Check if the scheduler is enabled (runtime-editable)."""
        return self._runtime_settings.get().scheduler_enabled

    @property
    def cron_expression(self) -> str:
        """Get the cron expression (runtime-editable)."""
        return self._runtime_settings.get().scheduler_cron

    @property
    def next_run_at(self) -> datetime | None:
        """Get next scheduled run time."""
        return self._next_run_at

    def _get_next_run_time(self) -> datetime:
        """Calculate next run time using croniter in configured timezone."""
        tz = self._settings.timezone
        cron = croniter(self.cron_expression, datetime.now(tz))
        next_time = cron.get_next(datetime)
        # Convert to UTC for storage/comparison
        if next_time.tzinfo is None:
            next_time = next_time.replace(tzinfo=tz)
        return next_time.astimezone(UTC)

    def notify_settings_changed(self) -> None:
        """Wake the loop so cron/enabled changes apply immediately."""
        self._wake_event.set()

    def start(self) -> None:
        """Start the scheduler background task."""
        if self._task is not None:
            return
        self._stop_event.clear()
        self._wake_event.clear()
        self._task = asyncio.create_task(self._run_loop())
        logger.info("Scheduler started")

    async def stop(self) -> None:
        """Stop the scheduler background task."""
        if self._task is None:
            return
        self._stop_event.set()
        self._wake_event.set()
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None
        self._next_run_at = None
        logger.info("Scheduler stopped")

    async def _run_loop(self) -> None:
        """Main scheduler loop."""
        while not self._stop_event.is_set():
            next_run = self._get_next_run_time()
            self._next_run_at = next_run if self.enabled else None
            wait_seconds = (next_run - datetime.now(UTC)).total_seconds()

            self._wake_event.clear()
            timed_out = False
            try:
                await asyncio.wait_for(
                    self._wake_event.wait(),
                    timeout=max(0, wait_seconds),
                )
            except TimeoutError:
                timed_out = True

            if self._stop_event.is_set():
                break
            if not timed_out:
                # Settings changed; recompute the next run with new cron/enabled.
                continue

            if self.enabled:
                await self._refresh_library()
                await self._sync_all_enabled()

    def _create_jobs_for_subscriptions(
        self, subscriptions: list[Subscription]
    ) -> list[str]:
        """Create sync jobs for given subscriptions."""
        job_ids: list[str] = []
        for subscription in subscriptions:
            try:
                job = self._job_executor.create_and_start_job(
                    subscription.url,
                    subscription.max_items,
                    JobSource.SCHEDULER,
                    subscription.id,
                    is_podcast=subscription.is_podcast,
                )
                if job is None:
                    logger.warning(
                        "Could not create job for %s (queue full)",
                        subscription.name,
                    )
                    continue

                job_ids.append(job.id)
                self._subscription_service.update(
                    subscription.id,
                    {"last_synced_at": datetime.now(UTC)},
                )
                logger.info(
                    "Created sync job %s for %s",
                    job.id[:8],
                    subscription.name,
                )
            except Exception:
                logger.exception(
                    "Failed to create job for %s",
                    subscription.name,
                )
        return job_ids

    async def _sync_all_enabled(self) -> list[str]:
        """Sync enabled subscriptions allowed by the current toggles."""
        return self._sync_enabled_subscriptions()

    def _allowed_subscriptions(self) -> list[Subscription]:
        """Enabled subscriptions allowed by the current toggles, oldest first."""
        config = self._runtime_settings.get()
        allowed = {SubscriptionOrigin.MANUAL}
        if config.auto_sync_liked:
            allowed.add(SubscriptionOrigin.LIKED)
        if config.auto_sync_saved_playlists:
            allowed.add(SubscriptionOrigin.LIBRARY)

        subscriptions = [
            subscription
            for subscription in self._subscription_service.list(enabled=True)
            if subscription.origin in allowed
        ]
        subscriptions.sort(
            key=lambda subscription: (
                subscription.last_synced_at is not None,
                (
                    subscription.last_synced_at.timestamp()
                    if subscription.last_synced_at
                    else 0.0
                ),
            )
        )
        return subscriptions

    def _sync_enabled_subscriptions(self) -> list[str]:
        """Create jobs for allowed subscriptions, capped for scheduler runs."""
        subscriptions = self._allowed_subscriptions()
        limited = subscriptions[: self._runtime_settings.get().max_jobs_per_run]
        if len(limited) < len(subscriptions):
            logger.info(
                "Scheduler job cap reached: syncing %d of %d subscriptions",
                len(limited),
                len(subscriptions),
            )
        return self._create_jobs_for_subscriptions(limited)

    async def _refresh_library(self) -> None:
        """Discover library content before syncing (best-effort)."""
        config = self._runtime_settings.get()
        if not (config.auto_sync_liked or config.auto_sync_saved_playlists):
            return
        try:
            result = await asyncio.to_thread(self._library_sync.sync)
        except Exception:
            logger.exception("Library discovery failed")
            return
        if result.error:
            logger.warning("Library discovery: %s", result.error)

    def sync_subscription(self, subscription_id: UUID) -> str | None:
        """Create sync job for a single subscription. Returns job_id or None."""
        try:
            subscription = self._subscription_service.get(subscription_id)
        except SubscriptionNotFoundError:
            return None

        job_ids = self._create_jobs_for_subscriptions([subscription])
        return job_ids[0] if job_ids else None

    def sync_all(self) -> list[str]:
        """Create sync jobs for all allowed enabled subscriptions.

        Manual "sync all" is not capped; the scheduler's per-run cap only
        applies to automatic runs.
        """
        return self._create_jobs_for_subscriptions(self._allowed_subscriptions())
