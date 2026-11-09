"""Tests for runtime-editable library sync settings."""

from pathlib import Path

from sqlalchemy.engine import Engine
from yubal_api.db.settings_repository import SettingsRepository
from yubal_api.services.runtime_settings import RuntimeSettingsService
from yubal_api.settings import Settings


class TestRuntimeSettingsService:
    def test_uses_environment_defaults(self, engine: Engine, tmp_path: Path) -> None:
        service = RuntimeSettingsService(
            SettingsRepository(engine),
            Settings(
                root=tmp_path,
                auto_sync_liked=True,
                auto_sync_saved_playlists=False,
                auto_sync_max_jobs_per_run=10,
                auto_sync_liked_max_items=500,
            ),
        )

        config = service.get()

        assert config.auto_sync_liked is True
        assert config.auto_sync_saved_playlists is False
        assert config.max_jobs_per_run == 10
        assert config.liked_max_items == 500

    def test_overrides_environment_defaults(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        service = RuntimeSettingsService(
            SettingsRepository(engine),
            Settings(root=tmp_path),
        )

        updated = service.update(
            {
                "auto_sync_liked": True,
                "auto_sync_saved_playlists": True,
                "max_jobs_per_run": 5,
                "liked_max_items": None,
            }
        )

        assert updated.auto_sync_liked is True
        assert updated.auto_sync_saved_playlists is True
        assert updated.max_jobs_per_run == 5
        assert updated.liked_max_items is None
        # A fresh instance (simulating an app restart) still sees the override.
        assert service.get() == updated

    def test_malformed_stored_json_falls_back_to_default(
        self, engine: Engine, tmp_path: Path
    ) -> None:
        repository = SettingsRepository(engine)
        repository.set_many({"auto_sync_liked": "{"})
        service = RuntimeSettingsService(repository, Settings(root=tmp_path))

        assert service.get().auto_sync_liked is False
