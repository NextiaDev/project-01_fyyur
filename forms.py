from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, ValidationError, Optional, Length
import phonenumbers
from models import Genre, State
from enum import Enum

# phone validation for US
def isValidPhoneState(form, field):
    try:
        phone = phonenumbers.parse(field.data, 'US')
        if not phonenumbers.is_possible_number(phone):
            raise ValidationError('Invalid phone number!')
    except Exception as e:
        raise ValidationError(e.args)

# states from db
def getStates():
    return State.query.with_entities(State.abbreviation, State.abbreviation).all()

# genres from db
def getGenres():
    return Genre.query.with_entities(Genre.name, Genre.name).all()

# Enum + Custom Validator for genre
class E_Genre(Enum):
  Alternative = 'Alternative'
  Blues = 'Blues'
  Classical = 'Classical'
  Country = 'Country'
  Electronic = 'Electronic'
  Folk = 'Folk'
  Funk = 'Funk'
  Hip_Hop = 'Hip-Hop'
  Heavy_Metal = 'Heavy Metal'
  Instrumental = 'Instrumental'
  Jazz = 'Jazz'
  Musical_Theatre = 'Musical Theatre'
  Pop = 'Pop'
  Punk = 'Punk'
  R_AND_B = 'R&B'
  Reggae = 'Reggae'
  Rock_n_Roll = 'Rock n Roll'
  Soul = 'Soul'
  Other = 'Other'
  
  @classmethod
  def choices(cls):
    return [ (choice.value, choice.value) for choice in cls ]

def isValidGenre(form, field):
    try:
        valid_genres = set([ (choice.value) for choice in E_Genre ])
        if not valid_genres.intersection(set(field.data)):
            raise ValidationError("Invalid Genre!")    
    except Exception as e:
        raise ValidationError(e.args)

class ShowForm(Form):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()],
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=getStates()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[isValidPhoneState, Optional()]
    )
    image_link = StringField(
        'image_link', validators=[Length(max=500), Optional()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(), isValidGenre],
        choices=getGenres()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )
    seeking_artist = BooleanField(
        'seeking_artist', validators=[ Optional()]
    ) 
    seeking_description = StringField(
        'seeking_description', validators=[ Optional()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=getStates()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[isValidPhoneState, Optional()]
    )
    image_link = StringField(
        'image_link', validators=[ Length(max=500), Optional()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(), isValidGenre],
        choices=getGenres()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]
    )
    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )
    seeking_venue = BooleanField(
        'seeking_venue', validators=[ Optional()]
    ) 
    seeking_description = StringField(
        'seeking_description', validators=[ Optional()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

