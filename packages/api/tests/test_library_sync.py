"""Tests for library discovery and subscription upsert."""

from pathlib import Path
from unittest.mock import MagicMock

from sqlalchemy.engine import Engine
from yubal_api.db.settings_repository import SettingsRepository
from yubal_api.db.subscription import Subscription, SubscriptionOrigin, SubscriptionType
from yubal_api.db.subscription_repository import SubscriptionRepository
from yubal_api.services.library_sync_service import (
    LIKED_PLAYLIST_TITLE,
    LIKED_PLAYLIST_URL,
    LibrarySyncService,
)
from yubal_api.services.runtime_settings import RuntimeSettingsService
from yubal_api.services.subscription_service import SubscriptionService
from yubal_api.settings import Settings


class FakeClient:
    def __init__(self, playlists: list[dict]) -> None:
        self._playlists = playlists
        self.calls = 0

    def get_library_playlists(self) -> list[dict]:
        self.calls += 1
        return self._playlists


def _service(
    engine: Engine,
    tmp_path: Path,
    *,
    playlists: list[dict] | None = None,
    liked: bool = True,
    saved: bool = True,
    cookies: bool = True,
    liked_max_items: int | None = None,
) -> tuple[LibrarySyncService, SubscriptionService, FakeClient]:
    repository = SubscriptionRepository(engine)
    runtime = RuntimeSettingsService(
        SettingsRepository(engine),
        Settings(
            root=tmp_path,
            auto_sync_liked=liked,
            auto_sync_saved_playlists=saved,
            auto_sync_liked_max_items=liked_max_items,
        ),
    )
    subscription_service = SubscriptionService(repository, MagicMock())
    client = FakeClient(playlists or [])
    cookies_path = tmp_path / "cookies.txt"
    if cookies:
        cookies_path.write_text("# Netscape HTTP Cookie File\n")
    service = LibrarySyncService(
        subscription_service,
        runtime,
        cookies_path if cookies else None,
        client_factory=lambda **_: client,
    )
    return service, subscription_service, client


def _manual(url: str, name: str = "manual") -> Subscription:
    return Subscription(
        type=SubscriptionType.PLAYLIST,
        url=url,
        name=name,
        origin=SubscriptionOrigin.MANUAL,
    )


class TestLibrarySync:
    def test_creates_liked_and_saved_playlist_subscriptions(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        playlists = [
            {
                "playlistId": "PL1",
                "title": "Mix",
                "thumbnails": [{"url": "https://img/1.jpg"}],
                "count": "3",
            }
        ]
        service, subscriptions, _ = _service(engine, tmp_path, playlists=playlists)

        result = service.sync()

        assert result.liked_created == 1
        assert result.playlists_created == 1
        liked = subscriptions.list(origin=SubscriptionOrigin.LIKED)
        library = subscriptions.list(origin=SubscriptionOrigin.LIBRARY)
        assert liked[0].url == LIKED_PLAYLIST_URL
        assert liked[0].name == LIKED_PLAYLIST_TITLE
        assert library[0].url.endswith("list=PL1")
        assert library[0].name == "Mix"
        assert library[0].thumbnail_url == "https://img/1.jpg"

    def test_is_idempotent_and_refreshes_titles(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        playlists = [{"playlistId": "PL1", "title": "Old", "thumbnails": []}]
        service, subscriptions, _ = _service(engine, tmp_path, playlists=playlists)
        first = service.sync()
        assert first.liked_created == 1
        assert first.playlists_created == 1

        playlists[0]["title"] = "New"
        second = service.sync()

        assert second.liked_created == 0
        assert second.playlists_created == 0
        assert second.updated == 1
        assert len(subscriptions.list()) == 2
        library = subscriptions.list(origin=SubscriptionOrigin.LIBRARY)
        assert library[0].name == "New"

    def test_manual_subscriptions_are_not_duplicated(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        repository = SubscriptionRepository(engine)
        repository.create(_manual(LIKED_PLAYLIST_URL, "My Liked"))
        repository.create(_manual("https://www.youtube.com/playlist?list=PL1"))
        service, subscriptions, _ = _service(
            engine,
            tmp_path,
            playlists=[{"playlistId": "PL1", "title": "Mix", "thumbnails": []}],
        )

        result = service.sync()

        assert result.liked_created == 0
        assert result.playlists_created == 0
        assert len(subscriptions.list()) == 2
        assert all(
            sub.origin is SubscriptionOrigin.MANUAL for sub in subscriptions.list()
        )

    def test_liked_cap_follows_runtime_setting(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        repository = SubscriptionRepository(engine)
        repository.create(
            Subscription(
                type=SubscriptionType.PLAYLIST,
                url=LIKED_PLAYLIST_URL,
                name=LIKED_PLAYLIST_TITLE,
                origin=SubscriptionOrigin.LIKED,
                max_items=100,
            )
        )
        service, subscriptions, _ = _service(
            engine, tmp_path, liked_max_items=500, saved=False
        )

        result = service.sync()

        assert result.updated == 1
        liked = subscriptions.list(origin=SubscriptionOrigin.LIKED)
        assert liked[0].max_items == 500

    def test_disabled_auto_subscription_stays_disabled(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        repository = SubscriptionRepository(engine)
        repository.create(
            Subscription(
                type=SubscriptionType.PLAYLIST,
                url="https://music.youtube.com/playlist?list=PL1",
                name="Old",
                origin=SubscriptionOrigin.LIBRARY,
                enabled=False,
            )
        )
        service, subscriptions, _ = _service(
            engine,
            tmp_path,
            playlists=[{"playlistId": "PL1", "title": "New", "thumbnails": []}],
            liked=False,
        )

        service.sync()

        library = subscriptions.list(origin=SubscriptionOrigin.LIBRARY)
        assert library[0].enabled is False

    def test_missing_cookies_reports_error_without_rows(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        service, subscriptions, client = _service(engine, tmp_path, cookies=False)

        result = service.sync()

        assert result.error is not None
        assert subscriptions.list() == []
        assert client.calls == 0

    def test_toggles_off_is_a_noop(self, engine: Engine, tmp_path: Path) -> None:
        service, subscriptions, client = _service(
            engine, tmp_path, liked=False, saved=False
        )

        result = service.sync()

        assert result.liked_created == 0
        assert result.playlists_created == 0
        assert subscriptions.list() == []
        assert client.calls == 0
