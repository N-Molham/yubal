"""Library auto-sync settings endpoints."""

import asyncio

from fastapi import APIRouter

from yubal_api.api.deps import LibrarySyncDep, RuntimeSettingsDep
from yubal_api.schemas.settings import (
    LibrarySyncSettingsResponse,
    LibrarySyncSettingsUpdate,
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=LibrarySyncSettingsResponse)
def get_library_sync_settings(
    runtime_settings: RuntimeSettingsDep,
) -> LibrarySyncSettingsResponse:
    """Get effective library auto-sync settings."""
    config = runtime_settings.get()
    return LibrarySyncSettingsResponse(**config.model_dump())


@router.patch("", response_model=LibrarySyncSettingsResponse)
async def update_library_sync_settings(
    data: LibrarySyncSettingsUpdate,
    runtime_settings: RuntimeSettingsDep,
    library_sync: LibrarySyncDep,
) -> LibrarySyncSettingsResponse:
    """Update library auto-sync settings.

    When either toggle ends up enabled, discovery runs immediately so the
    playlist list (and the next sync) reflects the library without waiting
    for the scheduler.
    """
    updated = await asyncio.to_thread(
        runtime_settings.update, _non_nullable_fields(data)
    )
    if updated.auto_sync_liked or updated.auto_sync_saved_playlists:
        await asyncio.to_thread(library_sync.sync)
    return LibrarySyncSettingsResponse(**updated.model_dump())


def _non_nullable_fields(data: LibrarySyncSettingsUpdate) -> dict[str, object]:
    """Drop explicit nulls for fields that cannot be null.

    ``liked_max_items`` is intentionally nullable (null = unlimited); the
    booleans and the job cap are not, and an explicit null should behave like
    "leave unchanged" instead of persisting an invalid value.
    """
    fields = data.model_dump(exclude_unset=True)
    for key in ("auto_sync_liked", "auto_sync_saved_playlists", "max_jobs_per_run"):
        if fields.get(key) is None:
            fields.pop(key, None)
    return fields
