"""add phone number

Revision ID: 85746f50c3b9
Revises: bb642210215d
Create Date: 2022-09-24 17:28:42.737188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85746f50c3b9'
down_revision = 'bb642210215d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###