"""add ondelete=Cascade for BookingsORM

Revision ID: 1417751a4cd4
Revises: 3e57686ce481
Create Date: 2025-01-19 18:19:12.341370

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1417751a4cd4"
down_revision: Union[str, None] = "3e57686ce481"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("bookings_user_id_fkey", "bookings", type_="foreignkey")
    op.drop_constraint("bookings_room_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(None, "bookings", "users", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(None, "bookings", "rooms", ["room_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key("bookings_room_id_fkey", "bookings", "rooms", ["room_id"], ["id"])
    op.create_foreign_key("bookings_user_id_fkey", "bookings", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###
