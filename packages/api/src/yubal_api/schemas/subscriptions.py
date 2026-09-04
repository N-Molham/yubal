"""Subscription request/response schemas."""

from uuid import UUID

from pydantic import BaseModel, Field
from yubal import Source

from yubal_api.db.subscription import SubscriptionType
from yubal_api.schemas.jobs import YouTubeMusicUrl
from yubal_api.schemas.types import UTCDateTime


class SubscriptionCreate(BaseModel):
    """Request to create a subscription."""

    url: YouTubeMusicUrl
    max_items: int | None = Field(default=None, ge=1, le=10000)


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
    created_at: UTCDateTime
    last_synced_at: UTCDateTime | None

    model_config = {"from_attributes": True}


class SubscriptionListResponse(BaseModel):
    """List of subscriptions response."""

    items: list[SubscriptionResponse]


class SyncResponse(BaseModel):
    """Response for sync operations."""

    job_ids: list[str]
