"""add user_id column

Revision ID: 4807a65b1ba7
Revises: bac7dae8795f
Create Date: 2024-02-25 16:05:46.408160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4807a65b1ba7'
down_revision = 'bac7dae8795f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_entry_user_id",  # Dodaj nazwę ograniczenia
            'user', 
            ['user_id'], 
            ['id']
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.drop_constraint('fk_entry_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
