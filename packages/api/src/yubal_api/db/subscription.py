"""Database models."""

from datetime import UTC, datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel
from yubal import Source


class SubscriptionType(StrEnum):
    """Type of content subscription."""

    PLAYLIST = "playlist"
    # ARTIST = "artist"  # future


class SubscriptionFields(TypedDict, total=False):
    """Partial update fields for a subscription."""

    enabled: bool
    name: str
    thumbnail_url: str | None
    last_synced_at: datetime


class Subscription(SQLModel, table=True):
    """A subscription to sync content from YouTube Music."""

    __tablename__ = "subscriptions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: SubscriptionType = Field(index=True)
    url: str = Field(unique=True, index=True)
    name: str = Field(max_length=200)
    enabled: bool = Field(default=True)
    max_items: int | None = Field(default=None, ge=1, le=10000)
    thumbnail_url: str | None = Field(default=None, max_length=2048)
    platform: Source = Field(default=Source.YOUTUBE_MUSIC)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_synced_at: datetime | None = Field(default=None)
