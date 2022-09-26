"""create post table

Revision ID: 78ae4b17c36d
Revises: 
Create Date: 2022-09-24 16:12:07.334862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78ae4b17c36d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable = False, primary_key = True),
    sa.Column('title',sa.String(), nullable = False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
