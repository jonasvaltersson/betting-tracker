"""autogenerated migration

Revision ID: 456d30967aa6
Revises: 
Create Date: 2019-10-05 21:14:54.177862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '456d30967aa6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
