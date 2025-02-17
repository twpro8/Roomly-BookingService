"""Add unique constraint name

Revision ID: 108cc887e267
Revises: fa775db5f312
Create Date: 2025-02-17 06:27:22.983414

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "108cc887e267"
down_revision: Union[str, None] = "fa775db5f312"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uix_facility_title", "facilities", ["title"])
    op.create_unique_constraint(None, "facilities", ["title"])
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=255),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.drop_constraint(None, "facilities", type_="unique")
    op.drop_constraint("uix_facility_title", "facilities", type_="unique")
