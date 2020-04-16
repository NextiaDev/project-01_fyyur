"""empty message

Revision ID: cfd3513d5ef5
Revises: 527b5c2ac652
Create Date: 2020-04-15 04:22:19.458029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd3513d5ef5'
down_revision = '527b5c2ac652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_column('Shows', 'venue_id')
    op.drop_column('Shows', 'artist_id')
    # ### end Alembic commands ###