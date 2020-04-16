"""add association table between venue and artist

Revision ID: 527b5c2ac652
Revises: e9b8d8473f07
Create Date: 2020-04-15 04:09:02.493271

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '527b5c2ac652'
down_revision = 'e9b8d8473f07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('Venue', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Artist', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['Artist'], ['Artist.id'], name='shows_Artist_fkey'),
    sa.ForeignKeyConstraint(['Venue'], ['Venue.id'], name='shows_Venue_fkey'),
    sa.PrimaryKeyConstraint('Venue', 'Artist', name='shows_pkey')
    )
    op.drop_table('Shows')
    # ### end Alembic commands ###
