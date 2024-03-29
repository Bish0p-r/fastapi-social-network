"""Move fields from UserProfile to User table, delete UserProfile

Revision ID: f67ad3d3981a
Revises: 6c96b1e074d8
Create Date: 2023-10-18 18:47:12.359516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f67ad3d3981a'
down_revision: Union[str, None] = '6c96b1e074d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile')
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('bio', sa.String(), nullable=True))
    op.add_column('users', sa.Column('privacy_settings', sa.Enum('PUBLIC', 'FRIENDS', 'PRIVATE', name='privacysettingsenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'privacy_settings')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'date_of_birth')
    op.create_table('user_profile',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('bio', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('privacy_settings', postgresql.ENUM('PUBLIC', 'FRIENDS', 'PRIVATE', name='privacysettingsenum'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_profile_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_profile_pkey'),
    sa.UniqueConstraint('user_id', name='user_profile_user_id_key')
    )
    # ### end Alembic commands ###
