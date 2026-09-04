"""add subscription platform

Revision ID: aa3cc7f9d164
Revises: 03132d5514f9
Create Date: 2026-09-04 15:23:09.439108

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa3cc7f9d164"
down_revision: str | Sequence[str] | None = "03132d5514f9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    Nullable-first-then-backfill so existing rows get a value before the
    column is made non-null — ALTER TABLE ADD COLUMN NOT NULL fails on a
    non-empty table otherwise. Backfill pattern-matches the URL rather than
    defaulting everything to youtube_music: this fork may already have
    SoundCloud/plain-YouTube subscriptions from before this column existed.

    Values are the enum MEMBER NAMES (e.g. "SOUNDCLOUD"), not `.value`
    ("soundcloud") — matches how SQLAlchemy's native Enum column type
    already stores the existing `type` column (SubscriptionType.PLAYLIST
    is stored as "PLAYLIST", confirmed against the live dev DB), so this
    stays consistent with that established convention.
    """
    op.add_column(
        "subscriptions",
        sa.Column("platform", sa.VARCHAR(), nullable=True),
    )
    op.execute(
        "UPDATE subscriptions SET platform = 'SOUNDCLOUD' "
        "WHERE url LIKE '%soundcloud.com%' AND platform IS NULL"
    )
    op.execute(
        "UPDATE subscriptions SET platform = 'YOUTUBE' "
        "WHERE url LIKE '%youtube%' AND url NOT LIKE '%music.youtube.com%' "
        "AND platform IS NULL"
    )
    op.execute(
        "UPDATE subscriptions SET platform = 'YOUTUBE_MUSIC' WHERE platform IS NULL"
    )
    with op.batch_alter_table("subscriptions") as batch_op:
        batch_op.alter_column("platform", existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("subscriptions", "platform")
