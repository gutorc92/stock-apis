"""Stock migration.

Revision ID: 958dc26b9123
Revises: 
Create Date: 2023-03-17 22:09:55.333340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '958dc26b9123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('base_ticket', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    # ### end Alembic commands ###