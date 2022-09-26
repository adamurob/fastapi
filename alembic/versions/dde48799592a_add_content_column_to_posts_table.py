"""add content column to posts table

Revision ID: dde48799592a
Revises: 78ae4b17c36d
Create Date: 2022-09-24 16:25:37.227987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dde48799592a'
down_revision = '78ae4b17c36d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
