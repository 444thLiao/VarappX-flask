"""empty message

Revision ID: 32c2cce0a678
Revises: 75ee7adfbef4
Create Date: 2017-04-24 13:21:02.718543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '32c2cce0a678'
down_revision = '75ee7adfbef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('db_access_id', sa.Integer(), nullable=True))
    op.drop_constraint('bookmarks_ibfk_1', 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'db_accesses', ['db_access_id'], ['id'])
    op.drop_column('bookmarks', 'db_access')
    op.add_column('db_accesses', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('db_accesses', sa.Column('variants_db_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'db_accesses', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'db_accesses', 'variants_db', ['variants_db_id'], ['id'])
    op.create_foreign_key(None, 'people', 'users', ['id'], ['id'])
    op.add_column('users', sa.Column('person_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'people', ['person_id'], ['id'])
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    op.drop_column('users', 'person_id')
    op.drop_constraint(None, 'people', type_='foreignkey')
    op.drop_constraint(None, 'db_accesses', type_='foreignkey')
    op.drop_constraint(None, 'db_accesses', type_='foreignkey')
    op.drop_column('db_accesses', 'variants_db_id')
    op.drop_column('db_accesses', 'user_id')
    op.add_column('bookmarks', sa.Column('db_access', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key('bookmarks_ibfk_1', 'bookmarks', 'db_accesses', ['db_access'], ['id'])
    op.drop_column('bookmarks', 'db_access_id')
    # ### end Alembic commands ###