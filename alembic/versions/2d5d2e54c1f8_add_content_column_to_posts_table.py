"""add content column to posts table

Revision ID: 2d5d2e54c1f8
Revises: 937fddfebb25
Create Date: 2024-03-03 11:02:23.406535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d5d2e54c1f8'
down_revision: Union[str, None] = '937fddfebb25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts', 
        sa.Column("content", sa.String(), nullable=False),
    )
    

def downgrade() -> None:
    op.drop_column('posts', column_name='content')
