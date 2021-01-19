"""empty message

Revision ID: 5f2cae1326d8
Revises: 3bfec0dd7aa2
Create Date: 2021-01-17 18:42:38.233531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f2cae1326d8'
down_revision = '3bfec0dd7aa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###