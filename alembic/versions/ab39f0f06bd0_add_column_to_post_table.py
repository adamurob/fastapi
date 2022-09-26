"""add column to post table

Revision ID: ab39f0f06bd0
Revises: bc09cc467142
Create Date: 2022-09-24 17:09:04.264862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab39f0f06bd0'
down_revision = 'bc09cc467142'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column ('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default ='True'),)
    op.add_column ('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
