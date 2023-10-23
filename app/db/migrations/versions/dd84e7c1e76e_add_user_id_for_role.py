"""add user_id for role

Revision ID: dd84e7c1e76e
Revises: 0ada55da7269
Create Date: 2023-10-23 16:42:47.932136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd84e7c1e76e'
down_revision: Union[str, None] = '0ada55da7269'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_roles', sa.Column('user_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'user_roles', 'users', ['user_id'], ['id'])
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_constraint(None, 'user_roles', type_='foreignkey')
    op.drop_column('user_roles', 'user_id')
    # ### end Alembic commands ###
