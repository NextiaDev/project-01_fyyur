"""add not null constraints to models

Revision ID: 5ec9068ad364
Revises: 252fd20773c5
Create Date: 2020-04-14 02:24:51.550979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5ec9068ad364'
down_revision = '252fd20773c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Album', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('Artist', 'state_fk',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Artist_availability', 'artist',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Artist_availability', 'date_time_end',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('Artist_availability', 'date_time_start',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('Genre', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Song', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('State', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Venue', 'seeking_artist',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('Venue', 'state_fk',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('Venue', 'state_fk',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Venue', 'seeking_artist',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('State', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Song', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Genre', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist_availability', 'date_time_start',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('Artist_availability', 'date_time_end',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('Artist_availability', 'artist',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Artist', 'state_fk',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Artist', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Album', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###