"""add ondelete cascade for rooms model

Revision ID: fa775db5f312
Revises: 1417751a4cd4
Create Date: 2025-02-08 19:41:49.489302

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "fa775db5f312"
down_revision: Union[str, None] = "1417751a4cd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("rooms_hotel_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key("rooms_hotel_id_fkey", "rooms", "hotels", ["hotel_id"], ["id"])
