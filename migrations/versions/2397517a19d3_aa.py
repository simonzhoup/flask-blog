"""aa

Revision ID: 2397517a19d3
Revises: 2aff952d0a8e
Create Date: 2017-12-13 10:35:16.642364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2397517a19d3'
down_revision = '2aff952d0a8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'answers', 'users', ['author'], ['id'])
    op.create_foreign_key(None, 'comment', 'users', ['author'], ['id'])
    op.create_foreign_key(None, 'messages', 'users', ['post_author_id'], ['id'])
    op.create_foreign_key(None, 'messages', 'users', ['from_id'], ['id'])
    op.create_foreign_key(None, 'messages', 'users', ['the_id'], ['id'])
    op.create_foreign_key(None, 'posts', 'users', ['author'], ['id'])
    op.create_foreign_key(None, 'questions', 'users', ['author'], ['id'])
    op.create_foreign_key(None, 'topicfollows', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'topics', 'users', ['author'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'topics', type_='foreignkey')
    op.drop_constraint(None, 'topicfollows', type_='foreignkey')
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'answers', type_='foreignkey')
    # ### end Alembic commands ###
