"""Discover library content and persist it as subscriptions.

Liked Music becomes a single ``LM`` subscription; every playlist saved in the
user's YouTube Music library becomes a ``LIBRARY`` subscription. Discovery is
idempotent: rows are matched by playlist ID, titles/thumbnails are refreshed
for auto-created rows, ``enabled`` is never overwritten, and the Liked Music
cap follows the runtime setting (manual rows are never touched).
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from yubal import AuthenticationRequiredError, UpstreamAPIError, parse_playlist_id
from yubal.client import YTMusicClient
from yubal.exceptions import PlaylistParseError

from yubal_api.db.subscription import (
    Subscription,
    SubscriptionFields,
    SubscriptionOrigin,
)
from yubal_api.services.runtime_settings import (
    LibrarySyncSettings,
    RuntimeSettingsService,
)
from yubal_api.services.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

LIKED_PLAYLIST_ID = "LM"
LIKED_PLAYLIST_URL = "https://music.youtube.com/playlist?list=LM"
LIKED_PLAYLIST_TITLE = "Liked Music"
PLAYLIST_URL_TEMPLATE = "https://music.youtube.com/playlist?list={playlist_id}"


class LibraryClient(Protocol):
    """Minimal YTMusic client surface used by discovery."""

    def get_library_playlists(self) -> list[dict[str, Any]]: ...


@dataclass
class LibrarySyncResult:
    """Outcome of one library discovery pass."""

    liked_created: int = 0
    playlists_created: int = 0
    updated: int = 0
    skipped: int = 0
    error: str | None = None


class LibrarySyncService:
    """Discover liked songs and saved playlists, upserting subscriptions."""

    def __init__(
        self,
        subscription_service: SubscriptionService,
        runtime_settings: RuntimeSettingsService,
        cookies_path: Path | None,
        client_factory: Callable[..., LibraryClient] = YTMusicClient,
    ) -> None:
        self._subscription_service = subscription_service
        self._runtime_settings = runtime_settings
        self._cookies_path = cookies_path
        self._client_factory = client_factory

    def sync(self) -> LibrarySyncResult:
        """Run discovery according to the effective toggles.

        Never raises: missing/expired cookies are reported through
        ``result.error`` so the scheduler can log and retry next run.
        """
        config = self._runtime_settings.get()
        if not (config.auto_sync_liked or config.auto_sync_saved_playlists):
            return LibrarySyncResult()

        if self._cookies_path is None or not self._cookies_path.exists():
            return LibrarySyncResult(
                error="YouTube Music cookies are required for library auto-sync"
            )

        result = LibrarySyncResult()
        existing = self._existing_by_playlist_id()
        client = self._client_factory(cookies_path=self._cookies_path)

        if config.auto_sync_liked:
            self._ensure_liked_subscription(existing, config, result)

        if config.auto_sync_saved_playlists:
            try:
                playlists = client.get_library_playlists()
            except (AuthenticationRequiredError, UpstreamAPIError) as e:
                result.error = str(e)
                logger.warning("Library playlist discovery failed: %s", e)
                return result
            self._sync_saved_playlists(playlists, existing, result)

        logger.info(
            "Library discovery: liked=%d created, playlists=%d created, "
            "%d updated, %d skipped",
            result.liked_created,
            result.playlists_created,
            result.updated,
            result.skipped,
        )
        return result

    def _existing_by_playlist_id(self) -> dict[str, Subscription]:
        by_id: dict[str, Subscription] = {}
        for subscription in self._subscription_service.list():
            try:
                playlist_id = parse_playlist_id(subscription.url)
            except PlaylistParseError:
                continue
            by_id.setdefault(playlist_id, subscription)
        return by_id

    def _ensure_liked_subscription(
        self,
        existing: dict[str, Subscription],
        config: LibrarySyncSettings,
        result: LibrarySyncResult,
    ) -> None:
        subscription = existing.get(LIKED_PLAYLIST_ID)
        if subscription is not None:
            # Manual LM subscriptions stay manual (and always sync).
            if subscription.origin is SubscriptionOrigin.MANUAL:
                result.skipped += 1
                return

            fields: SubscriptionFields = {}
            if subscription.name != LIKED_PLAYLIST_TITLE:
                fields["name"] = LIKED_PLAYLIST_TITLE
            if subscription.max_items != config.liked_max_items:
                fields["max_items"] = config.liked_max_items
            if fields:
                self._subscription_service.update(subscription.id, fields)
                result.updated += 1
            else:
                result.skipped += 1
            return

        self._subscription_service.create_auto(
            LIKED_PLAYLIST_URL,
            LIKED_PLAYLIST_TITLE,
            SubscriptionOrigin.LIKED,
            max_items=config.liked_max_items,
        )
        result.liked_created += 1

    def _sync_saved_playlists(
        self,
        playlists: list[dict],
        existing: dict[str, Subscription],
        result: LibrarySyncResult,
    ) -> None:
        for item in playlists:
            playlist_id = item.get("playlistId")
            if not playlist_id or playlist_id == LIKED_PLAYLIST_ID:
                result.skipped += 1
                continue

            title = str(item.get("title") or "Unknown Playlist")
            thumbnail_url = _last_thumbnail(item)
            subscription = existing.get(str(playlist_id))

            if subscription is None:
                self._subscription_service.create_auto(
                    PLAYLIST_URL_TEMPLATE.format(playlist_id=playlist_id),
                    title,
                    SubscriptionOrigin.LIBRARY,
                    thumbnail_url=thumbnail_url,
                )
                result.playlists_created += 1
                continue

            if subscription.origin is SubscriptionOrigin.MANUAL:
                result.skipped += 1
                continue

            fields: SubscriptionFields = {}
            if subscription.name != title:
                fields["name"] = title
            if thumbnail_url and subscription.thumbnail_url != thumbnail_url:
                fields["thumbnail_url"] = thumbnail_url
            if fields:
                self._subscription_service.update(subscription.id, fields)
                result.updated += 1
            else:
                result.skipped += 1


def _last_thumbnail(item: dict) -> str | None:
    thumbnails = item.get("thumbnails") or []
    for thumbnail in reversed(thumbnails):
        if isinstance(thumbnail, dict) and thumbnail.get("url"):
            return str(thumbnail["url"])
    return None
