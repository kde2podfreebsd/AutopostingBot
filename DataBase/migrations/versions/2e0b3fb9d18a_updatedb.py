"""updatedb

Revision ID: 2e0b3fb9d18a
Revises: 85415f93c43c
Create Date: 2023-07-17 20:54:48.989325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e0b3fb9d18a'
down_revision = '85415f93c43c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chains', sa.Column('chat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chains', 'users', ['chat_id'], ['chat_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chains', type_='foreignkey')
    op.drop_column('chains', 'chat_id')
    # ### end Alembic commands ###
