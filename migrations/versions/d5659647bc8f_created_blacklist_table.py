"""Created Blacklist table

Revision ID: d5659647bc8f
Revises: 1b521553b1f6
Create Date: 2023-10-19 17:14:49.735755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5659647bc8f'
down_revision: Union[str, None] = '1b521553b1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('initiator_user', sa.Integer(), nullable=True),
    sa.Column('blocked_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blocked_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['initiator_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('initiator_user', 'blocked_user')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    # ### end Alembic commands ###
