"""Create a baseline migrations 2

Revision ID: 13f6f3f343bf
Revises: 1034c7ad9add
Create Date: 2023-10-20 11:18:30.180542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13f6f3f343bf'
down_revision: Union[str, None] = '1034c7ad9add'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###