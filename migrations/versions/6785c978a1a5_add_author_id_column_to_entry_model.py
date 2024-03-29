"""Add author_id column to Entry model

Revision ID: 6785c978a1a5
Revises: 4807a65b1ba7
Create Date: 2024-02-25 16:34:21.997499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6785c978a1a5'
down_revision = '4807a65b1ba7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_entry_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_entry_author_id', 'user', ['author_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_entry_author_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_entry_user_id', 'user', ['user_id'], ['id'])
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###
