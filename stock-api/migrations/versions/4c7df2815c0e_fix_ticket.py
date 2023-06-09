"""Fix ticket

Revision ID: 4c7df2815c0e
Revises: 176102e887d0
Create Date: 2023-03-22 17:55:52.918527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c7df2815c0e'
down_revision = '176102e887d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ticket_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('transaction_tick_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ticket', ['ticket_id'], ['id'])
        batch_op.drop_column('tick_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tick_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('transaction_tick_id_fkey', 'ticket', ['tick_id'], ['id'])
        batch_op.drop_column('ticket_id')

    # ### end Alembic commands ###
