"""Library auto-sync settings schemas."""

from pydantic import BaseModel, Field


class LibrarySyncSettingsResponse(BaseModel):
    """Effective library auto-sync settings."""

    auto_sync_liked: bool
    auto_sync_saved_playlists: bool
    max_jobs_per_run: int
    liked_max_items: int | None


class LibrarySyncSettingsUpdate(BaseModel):
    """Partial update for library auto-sync settings."""

    auto_sync_liked: bool | None = None
    auto_sync_saved_playlists: bool | None = None
    max_jobs_per_run: int | None = Field(default=None, ge=1, le=200)
    liked_max_items: int | None = Field(default=None, ge=1, le=10000)
