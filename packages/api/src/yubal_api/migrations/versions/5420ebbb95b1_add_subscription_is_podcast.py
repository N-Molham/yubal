"""add subscription is_podcast

Revision ID: 5420ebbb95b1
Revises: aa3cc7f9d164
Create Date: 2026-09-04 15:47:15.615487

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5420ebbb95b1"
down_revision: str | Sequence[str] | None = "aa3cc7f9d164"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    A plain boolean default (unlike platform's URL-dependent backfill)
    works fine as a server_default — existing subscriptions safely default
    to "not a podcast" (False).
    """
    op.add_column(
        "subscriptions",
        sa.Column(
            "is_podcast", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("subscriptions", "is_podcast")
