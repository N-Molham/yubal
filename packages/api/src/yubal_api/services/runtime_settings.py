"""Runtime-editable library auto-sync settings.

Environment variables provide defaults; ``app_settings`` rows store overrides
saved from the web UI. The scheduler reads the effective values on every run,
so changes apply without a restart.
"""

import json
import logging
from typing import Any

from pydantic import BaseModel, Field

from yubal_api.db.settings_repository import SettingsRepository
from yubal_api.settings import Settings

logger = logging.getLogger(__name__)


class LibrarySyncSettings(BaseModel):
    """Effective library auto-sync configuration."""

    auto_sync_liked: bool
    auto_sync_saved_playlists: bool
    max_jobs_per_run: int = Field(ge=1, le=200)
    liked_max_items: int | None = Field(default=None, ge=1, le=10000)


class RuntimeSettingsService:
    """Merge environment defaults with runtime overrides from the database."""

    _KEYS = (
        "auto_sync_liked",
        "auto_sync_saved_playlists",
        "max_jobs_per_run",
        "liked_max_items",
    )

    def __init__(self, repository: SettingsRepository, defaults: Settings) -> None:
        self._repository = repository
        self._defaults = defaults

    def get(self) -> LibrarySyncSettings:
        """Return the effective settings (overrides layered over env defaults)."""
        overrides = self._repository.get_all()
        return LibrarySyncSettings(
            auto_sync_liked=self._read(
                overrides, "auto_sync_liked", self._defaults.auto_sync_liked
            ),
            auto_sync_saved_playlists=self._read(
                overrides,
                "auto_sync_saved_playlists",
                self._defaults.auto_sync_saved_playlists,
            ),
            max_jobs_per_run=self._read(
                overrides,
                "max_jobs_per_run",
                self._defaults.auto_sync_max_jobs_per_run,
            ),
            liked_max_items=self._read(
                overrides,
                "liked_max_items",
                self._defaults.auto_sync_liked_max_items,
            ),
        )

    def update(self, fields: dict[str, Any]) -> LibrarySyncSettings:
        """Persist the provided override fields and return effective settings."""
        values = {
            key: json.dumps(value) for key, value in fields.items() if key in self._KEYS
        }
        self._repository.set_many(values)
        return self.get()

    @staticmethod
    def _read(overrides: dict[str, str], key: str, default: Any) -> Any:
        raw = overrides.get(key)
        if raw is None:
            return default
        try:
            return json.loads(raw)
        except (TypeError, ValueError):
            logger.warning("Invalid stored value for setting %s: %r", key, raw)
            return default
