"""add subscription origin and runtime settings

Revision ID: 9f1b7c2d4a60
Revises: 5420ebbb95b1
Create Date: 2026-11-09 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f1b7c2d4a60"
down_revision: str | Sequence[str] | None = "5420ebbb95b1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    ``origin`` is stored as the enum MEMBER NAME (e.g. "MANUAL"), matching
    the existing ``type``/``platform`` columns. Existing rows are manual by
    definition (they predate library discovery).

    ``app_settings`` holds runtime overrides for library auto-sync toggles,
    layered over the environment defaults.
    """
    op.add_column(
        "subscriptions",
        sa.Column(
            "origin",
            sa.VARCHAR(),
            nullable=False,
            server_default="MANUAL",
        ),
    )
    op.create_table(
        "app_settings",
        sa.Column("key", sa.VARCHAR(length=100), primary_key=True),
        sa.Column("value", sa.VARCHAR(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("app_settings")
    op.drop_column("subscriptions", "origin")
