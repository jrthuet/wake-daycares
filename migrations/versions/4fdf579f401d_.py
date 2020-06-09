"""empty message

Revision ID: 4fdf579f401d
Revises: 25bd2e34ee4b
Create Date: 2020-05-21 23:50:32.189674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fdf579f401d'
down_revision = '25bd2e34ee4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('coords', sa.Numeric(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'coords')
    # ### end Alembic commands ###
