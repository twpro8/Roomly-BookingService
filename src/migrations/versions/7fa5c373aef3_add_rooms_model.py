"""add rooms model

Revision ID: 7fa5c373aef3
Revises: 1af8379560df
Create Date: 2024-12-28 20:04:19.831437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fa5c373aef3'
down_revision: Union[str, None] = '1af8379560df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_hotel', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_hotel'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
