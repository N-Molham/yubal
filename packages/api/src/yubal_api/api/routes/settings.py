"""Application settings endpoints."""

import asyncio

from fastapi import APIRouter

from yubal_api.api.deps import (
    LibrarySyncDep,
    RuntimeSettingsDep,
    SchedulerDep,
    SettingsDep,
)
from yubal_api.schemas.settings import (
    EnvironmentSettings,
    SettingsResponse,
    SettingsUpdate,
)
from yubal_api.services.runtime_settings import RuntimeSettings
from yubal_api.settings import Settings

router = APIRouter(prefix="/settings", tags=["settings"])


def _environment(settings: Settings) -> EnvironmentSettings:
    return EnvironmentSettings(
        root=settings.root,
        data=settings.data,
        config=settings.config,
        base_path=settings.base_path,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        debug=settings.debug,
        log_level=settings.log_level,
        temp=settings.temp,
        cors_origins=settings.cors_origins,
        tz=settings.tz,
    )


def _response(config: RuntimeSettings, settings: Settings) -> SettingsResponse:
    return SettingsResponse(**config.model_dump(), environment=_environment(settings))


@router.get("", response_model=SettingsResponse)
def get_settings(
    runtime_settings: RuntimeSettingsDep,
    settings: SettingsDep,
) -> SettingsResponse:
    """Get effective settings and the read-only environment block."""
    return _response(runtime_settings.get(), settings)


@router.patch("", response_model=SettingsResponse)
async def update_settings(
    data: SettingsUpdate,
    runtime_settings: RuntimeSettingsDep,
    library_sync: LibrarySyncDep,
    scheduler: SchedulerDep,
    settings: SettingsDep,
) -> SettingsResponse:
    """Update runtime-editable settings.

    Scheduler changes wake the scheduler so a new cron/enabled value takes
    effect immediately. Enabling library sync runs discovery right away.
    """
    fields = _fields_without_nulls(data)
    updated = await asyncio.to_thread(runtime_settings.update, fields)

    scheduler.notify_settings_changed()
    if updated.auto_sync_liked or updated.auto_sync_saved_playlists:
        await asyncio.to_thread(library_sync.sync)

    return _response(updated, settings)


def _fields_without_nulls(data: SettingsUpdate) -> dict[str, object]:
    """Drop explicit nulls except for the nullable Liked Music cap."""
    fields = data.model_dump(exclude_unset=True)
    for key in list(fields):
        if key != "liked_max_items" and fields[key] is None:
            fields.pop(key)
    return fields
