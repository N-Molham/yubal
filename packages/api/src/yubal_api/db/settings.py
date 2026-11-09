"""Database model for runtime-editable settings overrides."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class AppSetting(SQLModel, table=True):
    """A single runtime setting override, stored as JSON text.

    Environment variables provide the defaults; rows here override them.
    Values are JSON-encoded so booleans, integers and nulls round-trip.
    """

    __tablename__ = "app_settings"

    key: str = Field(primary_key=True, max_length=100)
    value: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
