"""Fix ticket

Revision ID: f4722e0d92c0
Revises: 4c7df2815c0e
Create Date: 2023-03-22 18:14:15.451286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f4722e0d92c0'
down_revision = '4c7df2815c0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('market', sa.Enum('frac', 'normal', name='market_type'), nullable=False))

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('market')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('market', postgresql.ENUM('frac', 'normal', name='market_type'), autoincrement=False, nullable=False))

    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_column('market')

    # ### end Alembic commands ###
