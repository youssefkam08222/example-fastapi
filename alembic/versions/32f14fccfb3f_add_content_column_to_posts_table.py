"""add content column to posts table

Revision ID: 32f14fccfb3f
Revises: ad50c91049df
Create Date: 2024-04-05 01:10:36.344368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32f14fccfb3f'
down_revision: Union[str, None] = 'ad50c91049df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
