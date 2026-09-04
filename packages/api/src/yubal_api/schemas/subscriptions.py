"""Subscription request/response schemas."""

from uuid import UUID

from pydantic import BaseModel, Field, model_validator
from yubal import Source, classify_source

from yubal_api.db.subscription import SubscriptionType
from yubal_api.schemas.jobs import YouTubeMusicUrl
from yubal_api.schemas.types import UTCDateTime


class SubscriptionCreate(BaseModel):
    """Request to create a subscription."""

    url: YouTubeMusicUrl
    max_items: int | None = Field(default=None, ge=1, le=10000)
    is_podcast: bool = Field(
        default=False,
        description="Treat synced content as podcast episodes, not music. "
        "Only valid for plain YouTube URLs (not YouTube Music or SoundCloud).",
    )

    @model_validator(mode="after")
    def _podcast_requires_youtube_source(self) -> "SubscriptionCreate":
        if self.is_podcast and classify_source(self.url) != Source.YOUTUBE:
            raise ValueError(
                "is_podcast is only valid for plain YouTube URLs, not "
                "YouTube Music or SoundCloud"
            )
        return self


class SubscriptionUpdate(BaseModel):
    """Request to update a subscription."""

    enabled: bool | None = None


class SubscriptionResponse(BaseModel):
    """Subscription response."""

    id: UUID
    type: SubscriptionType
    url: str = Field(json_schema_extra={"format": "uri"})
    name: str
    enabled: bool
    max_items: int | None
    thumbnail_url: str | None = Field(default=None, json_schema_extra={"format": "uri"})
    platform: Source
    is_podcast: bool
    created_at: UTCDateTime
    last_synced_at: UTCDateTime | None

    model_config = {"from_attributes": True}


class SubscriptionListResponse(BaseModel):
    """List of subscriptions response."""

    items: list[SubscriptionResponse]


class SyncResponse(BaseModel):
    """Response for sync operations."""

    job_ids: list[str]
