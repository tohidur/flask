"""followers

Revision ID: 629816b75f2f
Revises: aaab5334cc75
Create Date: 2020-11-01 09:25:46.168044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '629816b75f2f'
down_revision = 'aaab5334cc75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
