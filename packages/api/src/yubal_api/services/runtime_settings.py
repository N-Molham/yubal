"""Runtime-editable application settings.

Environment variables provide defaults; ``app_settings`` rows store overrides
saved from the web UI. Services read the effective values per job / scheduler
tick, so changes apply without a restart. Infrastructure settings (paths,
bind address, logging) remain environment-only and are shown read-only.
"""

import json
import logging
from typing import Any

from pydantic import BaseModel, Field
from yubal import AudioCodec

from yubal_api.db.settings_repository import SettingsRepository
from yubal_api.settings import CronExpression, Settings

logger = logging.getLogger(__name__)


class RuntimeSettings(BaseModel):
    """Settings that can be changed at runtime from the web UI."""

    # Downloads / metadata
    audio_format: AudioCodec
    audio_quality: int = Field(ge=0, le=10)
    fetch_lyrics: bool
    ytmusic_lyrics_fallback: bool
    ascii_filenames: bool
    download_ugc: bool
    replaygain: bool

    # Scheduler
    scheduler_enabled: bool
    scheduler_cron: CronExpression
    job_timeout_seconds: int = Field(ge=60)

    # Library auto-sync
    auto_sync_liked: bool
    auto_sync_saved_playlists: bool
    max_jobs_per_run: int = Field(ge=1, le=200)
    liked_max_items: int | None = Field(default=None, ge=1, le=10000)


# Backwards-compatible name used by the library-sync codepath.
LibrarySyncSettings = RuntimeSettings


class RuntimeSettingsService:
    """Merge environment defaults with runtime overrides from the database."""

    _KEYS = tuple(RuntimeSettings.model_fields)

    def __init__(self, repository: SettingsRepository, defaults: Settings) -> None:
        self._repository = repository
        self._defaults = defaults

    def get(self) -> RuntimeSettings:
        """Return the effective settings (overrides layered over env defaults)."""
        overrides = self._repository.get_all()
        defaults = self._defaults
        return RuntimeSettings(
            audio_format=self._read(overrides, "audio_format", defaults.audio_format),
            audio_quality=self._read(
                overrides, "audio_quality", int(defaults.audio_quality)
            ),
            fetch_lyrics=self._read(overrides, "fetch_lyrics", defaults.fetch_lyrics),
            ytmusic_lyrics_fallback=self._read(
                overrides,
                "ytmusic_lyrics_fallback",
                defaults.ytmusic_lyrics_fallback,
            ),
            ascii_filenames=self._read(
                overrides, "ascii_filenames", defaults.ascii_filenames
            ),
            download_ugc=self._read(overrides, "download_ugc", defaults.download_ugc),
            replaygain=self._read(overrides, "replaygain", defaults.replaygain),
            scheduler_enabled=self._read(
                overrides, "scheduler_enabled", defaults.scheduler_enabled
            ),
            scheduler_cron=self._read(
                overrides, "scheduler_cron", defaults.scheduler_cron
            ),
            job_timeout_seconds=self._read(
                overrides, "job_timeout_seconds", defaults.job_timeout_seconds
            ),
            auto_sync_liked=self._read(
                overrides, "auto_sync_liked", defaults.auto_sync_liked
            ),
            auto_sync_saved_playlists=self._read(
                overrides,
                "auto_sync_saved_playlists",
                defaults.auto_sync_saved_playlists,
            ),
            max_jobs_per_run=self._read(
                overrides,
                "max_jobs_per_run",
                defaults.auto_sync_max_jobs_per_run,
            ),
            liked_max_items=self._read(
                overrides,
                "liked_max_items",
                defaults.auto_sync_liked_max_items,
            ),
        )

    def update(self, fields: dict[str, Any]) -> RuntimeSettings:
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
