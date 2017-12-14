"""aa

Revision ID: 8b16a7c8e2cd
Revises: 08210e949047
Create Date: 2017-12-14 19:06:33.070373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b16a7c8e2cd'
down_revision = '08210e949047'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('activation', sa.Boolean(), nullable=True))
    op.add_column('comment', sa.Column('activation', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('activation', sa.Boolean(), nullable=True))
    op.drop_column('posts', 'ban')
    op.add_column('questions', sa.Column('activation', sa.Boolean(), nullable=True))
    op.add_column('topics', sa.Column('activation', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topics', 'activation')
    op.drop_column('questions', 'activation')
    op.add_column('posts', sa.Column('ban', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('posts', 'activation')
    op.drop_column('comment', 'activation')
    op.drop_column('answers', 'activation')
    # ### end Alembic commands ###
