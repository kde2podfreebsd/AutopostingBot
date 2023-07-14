"""update#1

Revision ID: 56378b9e5385
Revises: 95723a0b1eb5
Create Date: 2023-07-14 21:16:41.601916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56378b9e5385'
down_revision = '95723a0b1eb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_chains_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'chains_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('chains_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_chains_id_fkey', 'users', 'chains', ['chains_id'], ['chain_id'])
    # ### end Alembic commands ###
