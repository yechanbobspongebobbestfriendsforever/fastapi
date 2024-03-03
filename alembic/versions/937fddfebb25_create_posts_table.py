"""create posts table

Revision ID: 937fddfebb25
Revises: 
Create Date: 2024-03-03 10:53:53.572341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '937fddfebb25'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )
    
def downgrade() -> None:
    op.drop_table('posts')
    
