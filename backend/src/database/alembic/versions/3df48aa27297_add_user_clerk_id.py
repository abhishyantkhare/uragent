"""Add user clerk id

Revision ID: 3df48aa27297
Revises: d7d26dcce710
Create Date: 2024-10-18 18:03:13.572666

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3df48aa27297"
down_revision: Union[str, None] = "d7d26dcce710"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("clerk_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "clerk_id")
    # ### end Alembic commands ###
