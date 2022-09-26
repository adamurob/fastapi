"""add foreign-key to post table

Revision ID: bc09cc467142
Revises: 1fd7a72ef770
Create Date: 2022-09-24 16:59:44.012164

"""
from threading import local
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc09cc467142'
down_revision = '1fd7a72ef770'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_users_fk', source_table = "posts", referent_table = "users",
    local_cols=['owner_id'], remote_cols = ['id'], ondelete = "CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name = "posts")
    op.drop_column('posts','owner_id')
    pass
