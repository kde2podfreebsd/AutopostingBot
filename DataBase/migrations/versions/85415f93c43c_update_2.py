"""update#2

Revision ID: 85415f93c43c
Revises: 56378b9e5385
Create Date: 2023-07-14 22:05:44.373526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85415f93c43c'
down_revision = '56378b9e5385'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('post_text', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('post_date', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('media_files', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'media_files')
    op.drop_column('posts', 'post_date')
    op.drop_column('posts', 'post_text')
    # ### end Alembic commands ###