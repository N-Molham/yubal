"""Database repository for runtime setting overrides."""

from datetime import UTC, datetime

from sqlalchemy import Engine
from sqlmodel import Session, select

from yubal_api.db.settings import AppSetting


class SettingsRepository:
    """Repository for runtime setting overrides."""

    def __init__(self, engine: Engine) -> None:
        """Initialize repository with database engine."""
        self._engine = engine

    def get_all(self) -> dict[str, str]:
        """Return all stored overrides keyed by setting name."""
        with Session(self._engine) as session:
            rows = session.exec(select(AppSetting)).all()
            return {row.key: row.value for row in rows}

    def set_many(self, values: dict[str, str]) -> None:
        """Insert or update overrides in a single transaction."""
        if not values:
            return
        now = datetime.now(UTC)
        with Session(self._engine) as session:
            for key, value in values.items():
                existing = session.get(AppSetting, key)
                if existing is None:
                    session.add(AppSetting(key=key, value=value, updated_at=now))
                else:
                    existing.value = value
                    existing.updated_at = now
            session.commit()
