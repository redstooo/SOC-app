"""empty message

Revision ID: 304cac897cf9
Revises: 
Create Date: 2025-02-14 14:25:55.072997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304cac897cf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chemicals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state', sa.String(length=256), nullable=False))
        batch_op.create_unique_constraint(None, ['state'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chemicals', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('state')

    # ### end Alembic commands ###
