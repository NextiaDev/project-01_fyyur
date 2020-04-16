from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length, ValidationError, Optional
import phonenumbers
import re
from models import Genre, State

# phone validation format and lenght
def isValidPhone(form, field):
    if not re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", field.data) and len(field.data) > 10:
        raise ValidationError("Invalid phone number.")

# phone validation for US
def isValidPhoneState(form, field):
    try:
        input_number = phonenumbers.parse(field.data, 'US')
        if not phonenumbers.is_possible_number(input_number):
            raise ValidationError('Invalid phone number.')
    except Exception as e:
        raise ValidationError(e.args)

# states from db
def getStates():
    return State.query.with_entities(State.abbreviation, State.abbreviation).all()

# genres from db
def getGenres():
    return Genre.query.with_entities(Genre.name, Genre.name).all()



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
        'phone', validators=[isValidPhone, isValidPhoneState, Length(min=10, max=18), Optional()]
    )
    image_link = StringField(
        'image_link', validators=[ Optional()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
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
        'phone', validators=[isValidPhone, isValidPhoneState, Length(min=10, max=18), Optional()]
    )
    image_link = StringField(
        'image_link', validators=[ Optional()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=getGenres()
    )
    facebook_link = StringField(
        # TODO implement enum restriction 
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

