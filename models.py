#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from database import *

genres_venue = db.Table('genres_venue',
    db.Column('Venue', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('Genre', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
  )

genres_artist = db.Table('genres_artist',
    db.Column('Artist', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('Genre', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
  )

album_artist = db.Table('album_artist',
    db.Column('Artist', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('Album', db.Integer, db.ForeignKey('Album.id'), primary_key=True),
  )

class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    abbreviation = db.Column(db.String(6), nullable=False)

class Genre(db.Model):
  __tablename__ = 'Genre'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)

class Album(db.Model):
  __tablename__ = 'Album'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)

class Song(db.Model):
  __tablename__ = 'Song'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  #FK 
  album_fk = db.Column(db.Integer, db.ForeignKey('Album.id'))

# association model betteewn artist and venues
class Shows(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  #realationships
  artist = db.relationship("Artist", back_populates="venues")
  venue = db.relationship("Venue", back_populates="artists")


class Artist_availability(db.Model):
  __tablename__ = 'Artist_availability'
  id = db.Column(db.Integer, primary_key=True)
  date_time_start = db.Column(db.DateTime, nullable=False)
  date_time_end = db.Column(db.DateTime, nullable=False)
  #FK 
  artist = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

class Venue(db.Model):
    __tablename__ = 'Venue'
    # required fields (name, city/state, address genres)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False) 
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_artist = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(240), nullable=True)
    # Relationships
    genres = db.relationship('Genre', secondary=genres_venue, backref=db.backref('venues', lazy=True))
    artists = db.relationship("Shows", back_populates="venue", lazy='dynamic')
    # FK
    state_fk = db.Column(db.Integer, db.ForeignKey('State.id'), nullable=False)
    

class Artist(db.Model):
    __tablename__ = 'Artist'
    # required fields (name, city/state, genres, seeking venue)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(240), nullable=True)
    
    # relationships
    genres = db.relationship('Genre', secondary=genres_artist, backref=db.backref('artists', lazy=True))
    venues = db.relationship("Shows", back_populates="artist", lazy='dynamic')
    # FK
    state_fk = db.Column(db.Integer, db.ForeignKey('State.id'), nullable=False)
