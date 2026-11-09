"""Tests for the scheduler service."""

from datetime import UTC, datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest
from yubal_api.db.subscription import Subscription, SubscriptionOrigin, SubscriptionType
from yubal_api.services.runtime_settings import LibrarySyncSettings
from yubal_api.services.scheduler import Scheduler


@pytest.fixture
def scheduler(mock_settings: MagicMock) -> Scheduler:
    """Create scheduler with mocked dependencies."""
    subscription_service = MagicMock()
    job_executor = MagicMock()
    return Scheduler(
        subscription_service,
        job_executor,
        mock_settings,
        library_sync=MagicMock(),
        runtime_settings=MagicMock(),
    )


class TestGetNextRunTime:
    """Tests for _get_next_run_time calculation."""

    def test_calculates_next_run_in_utc(
        self, scheduler: Scheduler, mock_settings: MagicMock
    ) -> None:
        """Should calculate next run time and return in UTC."""
        mock_settings.scheduler_cron = "0 * * * *"  # Every hour
        mock_settings.timezone = ZoneInfo("UTC")

        next_run = scheduler._get_next_run_time()

        assert next_run.tzinfo == UTC
        assert next_run > datetime.now(UTC)
        # Should be at minute 0 (top of hour)
        assert next_run.minute == 0
        assert next_run.second == 0

    def test_respects_configured_timezone(
        self, scheduler: Scheduler, mock_settings: MagicMock
    ) -> None:
        """Should evaluate cron in configured timezone."""
        # Set timezone to UTC+1
        tz = ZoneInfo("Europe/Paris")
        mock_settings.timezone = tz
        mock_settings.scheduler_cron = "0 */6 * * *"  # Every 6 hours

        next_run = scheduler._get_next_run_time()

        # Result should be in UTC
        assert next_run.tzinfo == UTC

        # Convert to local timezone to verify cron was evaluated correctly
        next_run_local = next_run.astimezone(tz)
        # Should be at hour 0, 6, 12, or 18 in local time
        assert next_run_local.hour in (0, 6, 12, 18)
        assert next_run_local.minute == 0

    def test_next_run_is_in_future(
        self, scheduler: Scheduler, mock_settings: MagicMock
    ) -> None:
        """Should always return a future time."""
        mock_settings.scheduler_cron = "* * * * *"  # Every minute
        mock_settings.timezone = ZoneInfo("UTC")

        next_run = scheduler._get_next_run_time()

        assert next_run > datetime.now(UTC)

    def test_different_timezones_produce_different_utc_times(
        self, mock_settings: MagicMock
    ) -> None:
        """Same cron in different timezones should produce different UTC times."""
        subscription_service = MagicMock()
        job_executor = MagicMock()

        # Scheduler with UTC
        mock_settings.timezone = ZoneInfo("UTC")
        mock_settings.scheduler_cron = "0 12 * * *"  # Noon
        scheduler_utc = Scheduler(
            subscription_service,
            job_executor,
            mock_settings,
            library_sync=MagicMock(),
            runtime_settings=MagicMock(),
        )
        next_utc = scheduler_utc._get_next_run_time()

        # Scheduler with Tokyo (UTC+9)
        mock_settings_tokyo = MagicMock()
        mock_settings_tokyo.scheduler_enabled = True
        mock_settings_tokyo.scheduler_cron = "0 12 * * *"  # Noon
        mock_settings_tokyo.timezone = ZoneInfo("Asia/Tokyo")
        scheduler_tokyo = Scheduler(
            subscription_service,
            job_executor,
            mock_settings_tokyo,
            library_sync=MagicMock(),
            runtime_settings=MagicMock(),
        )
        next_tokyo = scheduler_tokyo._get_next_run_time()

        # Noon in Tokyo is 3am UTC, noon in UTC is 12pm UTC
        # They should differ by ~9 hours (depending on current time)
        diff = abs((next_utc - next_tokyo).total_seconds())
        # Allow for day wraparound - diff should be ~9h or ~15h (24-9)
        assert diff in range(8 * 3600, 10 * 3600) or diff in range(14 * 3600, 16 * 3600)


def _subscription(
    url: str,
    origin: SubscriptionOrigin,
    *,
    last_synced_at: datetime | None = None,
) -> Subscription:
    return Subscription(
        type=SubscriptionType.PLAYLIST,
        url=url,
        name=url,
        origin=origin,
        last_synced_at=last_synced_at,
    )


def _scheduler_with(
    subscriptions: list[Subscription],
    *,
    liked: bool,
    saved: bool,
    max_jobs: int = 25,
    mock_settings: MagicMock | None = None,
) -> tuple[Scheduler, MagicMock]:
    subscription_service = MagicMock()
    subscription_service.list.return_value = subscriptions
    job_executor = MagicMock()
    job_executor.create_and_start_job.return_value = MagicMock(id="job")
    runtime_settings = MagicMock()
    runtime_settings.get.return_value = LibrarySyncSettings(
        auto_sync_liked=liked,
        auto_sync_saved_playlists=saved,
        max_jobs_per_run=max_jobs,
        liked_max_items=None,
    )
    scheduler = Scheduler(
        subscription_service,
        job_executor,
        mock_settings or MagicMock(),
        library_sync=MagicMock(),
        runtime_settings=runtime_settings,
    )
    return scheduler, job_executor


class TestLibraryOriginFiltering:
    """Scheduler must pause auto origins when their toggle is off."""

    def test_toggles_off_only_syncs_manual(self) -> None:
        scheduler, executor = _scheduler_with(
            [
                _subscription("u-manual", SubscriptionOrigin.MANUAL),
                _subscription("u-liked", SubscriptionOrigin.LIKED),
                _subscription("u-library", SubscriptionOrigin.LIBRARY),
            ],
            liked=False,
            saved=False,
        )

        scheduler._sync_enabled_subscriptions()

        urls = [c.args[0] for c in executor.create_and_start_job.call_args_list]
        assert urls == ["u-manual"]

    def test_toggles_on_include_auto_origins(self) -> None:
        scheduler, executor = _scheduler_with(
            [
                _subscription("u-manual", SubscriptionOrigin.MANUAL),
                _subscription("u-liked", SubscriptionOrigin.LIKED),
                _subscription("u-library", SubscriptionOrigin.LIBRARY),
            ],
            liked=True,
            saved=True,
        )

        scheduler._sync_enabled_subscriptions()

        urls = [c.args[0] for c in executor.create_and_start_job.call_args_list]
        assert set(urls) == {"u-manual", "u-liked", "u-library"}

    def test_cap_prefers_never_synced_then_oldest(self) -> None:
        scheduler, executor = _scheduler_with(
            [
                _subscription(
                    "u-new",
                    SubscriptionOrigin.MANUAL,
                    last_synced_at=datetime(2026, 1, 2, tzinfo=UTC),
                ),
                _subscription("u-never", SubscriptionOrigin.MANUAL),
                _subscription(
                    "u-old",
                    SubscriptionOrigin.MANUAL,
                    last_synced_at=datetime(2026, 1, 1, tzinfo=UTC),
                ),
            ],
            liked=False,
            saved=False,
            max_jobs=2,
        )

        scheduler._sync_enabled_subscriptions()

        urls = [c.args[0] for c in executor.create_and_start_job.call_args_list]
        assert urls == ["u-never", "u-old"]
