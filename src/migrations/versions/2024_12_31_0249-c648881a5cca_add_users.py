"""add users

Revision ID: c648881a5cca
Revises: ce6e2c2692ec
Create Date: 2024-12-31 02:49:33.609795

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c648881a5cca"
down_revision: Union[str, None] = "ce6e2c2692ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("bio", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("users")
