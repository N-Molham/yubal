"""Application settings schemas."""

from pathlib import Path

from pydantic import BaseModel, Field
from yubal import AudioCodec

from yubal_api.services.runtime_settings import RuntimeSettings
from yubal_api.settings import CronExpression


class EnvironmentSettings(BaseModel):
    """Environment-only settings, shown in the UI but restart-required."""

    root: Path
    data: Path
    config: Path
    base_path: str
    host: str
    port: int
    reload: bool
    debug: bool
    log_level: str
    temp: Path
    cors_origins: list[str]
    tz: str


class SettingsResponse(RuntimeSettings):
    """Effective runtime settings plus the read-only environment block."""

    environment: EnvironmentSettings


class SettingsUpdate(BaseModel):
    """Partial update for runtime-editable settings."""

    audio_format: AudioCodec | None = None
    audio_quality: int | None = Field(default=None, ge=0, le=10)
    fetch_lyrics: bool | None = None
    ytmusic_lyrics_fallback: bool | None = None
    ascii_filenames: bool | None = None
    download_ugc: bool | None = None
    replaygain: bool | None = None

    scheduler_enabled: bool | None = None
    scheduler_cron: CronExpression | None = None
    job_timeout_seconds: int | None = Field(default=None, ge=60)

    auto_sync_liked: bool | None = None
    auto_sync_saved_playlists: bool | None = None
    max_jobs_per_run: int | None = Field(default=None, ge=1, le=200)
    liked_max_items: int | None = Field(default=None, ge=1, le=10000)
