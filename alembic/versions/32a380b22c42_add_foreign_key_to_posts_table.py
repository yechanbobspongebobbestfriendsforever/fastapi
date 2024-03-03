"""add foreign-key to posts table

Revision ID: 32a380b22c42
Revises: 65fceb002af0
Create Date: 2024-03-03 11:14:45.065096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a380b22c42'
down_revision: Union[str, None] = '65fceb002af0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'posts', 
        sa.Column('owner_id', sa.Integer(),
                  nullable=False)
    )
    op.create_foreign_key(
        'post_users_fk',
        source_table="posts", 
        referent_table="users",
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass