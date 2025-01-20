"""add ondelete=Cascade for Rooms Facilities Orm

Revision ID: 3e57686ce481
Revises: c0ad1e45d391
Create Date: 2025-01-19 18:14:20.739740

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3e57686ce481"
down_revision: Union[str, None] = "c0ad1e45d391"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "rooms_facilities_room_id_fkey", "rooms_facilities", type_="foreignkey"
    )
    op.drop_constraint(
        "rooms_facilities_facility_id_fkey", "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        "rooms_facilities_facility_id_fkey",
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
    )
    op.create_foreign_key(
        "rooms_facilities_room_id_fkey",
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )
    # ### end Alembic commands ###
