"""Created Posts DateTime fields

Revision ID: d322759d7e69
Revises: 4485da1051ec
Create Date: 2023-10-20 19:44:39.279087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd322759d7e69'
down_revision: Union[str, None] = '4485da1051ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    # ### end Alembic commands ###
