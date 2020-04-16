#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from os import sys
from forms import *
from database import *
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  # get groups by city/state
  cities_states = db.session.query(Venue.city, Venue.state_fk).group_by(Venue.city, Venue.state_fk).all()
  data = []

  # venues by city/state
  for city, state_id in cities_states:
    q_venues = Venue.query.filter_by(city=city,state_fk=state_id)
    
    # venues data + upcoming shows count
    venues_data = []
    for venue in q_venues:
      shows = venue.artists
      upcoming_shows = shows.filter(Shows.start_time > datetime.now()).count()
      venue_dict = venue.__dict__
      venue_dict['upcoming_shows'] = upcoming_shows
      venues_data.append(venue_dict)

    # data by location
    state = State.query.get(state_id)

    d = {
      "city" : city,
      "state": state.abbreviation,
      "venues": venues_data
    }
    data.append(d)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  # search by venue name (convert search word and venue name to lower case for case-insensitive search with "contains")
  search_term= request.form.get('search_term', '').lower()
  search_results = Venue.query.filter(func.lower(Venue.name).contains(search_term))
  search_count = search_results.count()
  
  data_search = []

  # append results to data_search
  for venue in search_results:
    result_dict = {
      "id": venue.id,
      "name": venue.name,
    }
    data_search.append(result_dict)

  response={
    "count": search_count,
    "data": data_search
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  # query venue by id
  venue = Venue.query.get_or_404(venue_id)
  shows = venue.artists
  # venue result to dict, need to add extra data from shows
  venue_dict = venue.__dict__
  
  # query venue shows
  now =  datetime.now()
  past_shows = shows.filter(Shows.start_time < now)
  upcoming_shows = shows.filter(Shows.start_time > now)

  venue_dict['past_shows'] = past_shows.all()
  venue_dict['past_shows_count'] = past_shows.count()
  venue_dict['upcoming_shows'] = upcoming_shows.all()
  venue_dict['upcoming_shows_count'] = upcoming_shows.count()

  return render_template('pages/show_venue.html', venue=venue_dict)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)

  if form.validate():
    error_add_new_venue = 'No_error'

    try:
      data_venue = {}

      name = request.form['name']
      city = request.form['city']
      phone = request.form.get('phone') or None
      address = request.form.get('address')
      facebook_link = request.form.get('facebook_link') or None
      website_link = request.form.get('website_link') or None
      seeking_description = request.form.get('seeking_description') or None
      seeking_artist = request.form.get('seeking_artist') or None
      image_link = request.form.get('image_link') or None


      if seeking_artist is None:
        seeking_artist = False
      else:
        seeking_artist = True

      # get state object
      state = request.form.get('state')
      artist_state = State.query.filter_by(abbreviation=state).first_or_404()

      # new venue
      new_venue = Venue(name=name, city=city, address=address, phone=phone, facebook_link=facebook_link, website_link=website_link,
                    seeking_description=seeking_description, seeking_artist=seeking_artist, image_link=image_link,
                    state_fk=artist_state.id)

      # save for use after commit
      data_venue['name']= new_venue.name
      
      db.session.add(new_venue)
      db.session.commit()
      
    except:
      error_add_new_venue = 'Error_db_add'
      db.session.rollback()
      
    finally:
      db.session.close()
  else:
      error_add_new_venue = 'Error_form'
  
  # error flash mensages
  if error_add_new_venue == 'No_error':
    flash('Venue ' + data_venue['name'] + ' was successfully added!')
  elif error_add_new_venue == 'Error_db_add':
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be added.')
  elif error_add_new_venue == 'Error_form':
    flash('Error, Invalid Form!')
    print(form.errors)

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  # search by artist name (convert search word and artist name to lower case for case-insensitive search with "contains")
  search_term= request.form.get('search_term', '').lower()
  search_results = Artist.query.filter(func.lower(Artist.name).contains(search_term))
  search_count = search_results.count()
  
  data_search = []
  # append results to data_search
  for artist in search_results:
    result_dict = {
      "id": artist.id,
      "name": artist.name,
    }
    data_search.append(result_dict)

  response={
    "count": search_count,
    "data": data_search
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  # query venue by id
  artist = Artist.query.get_or_404(artist_id)
  shows = artist.venues 
  
  # artist result to dict, need to add extra data from shows
  artist_dict = artist.__dict__
  
  # query artist shows
  now =  datetime.now()
  past_shows = shows.filter(Shows.start_time < now)
  upcoming_shows = shows.filter(Shows.start_time > now)

  artist_dict['past_shows'] = past_shows.all()
  artist_dict['past_shows_count'] = past_shows.count()
  artist_dict['upcoming_shows'] = upcoming_shows.all()
  artist_dict['upcoming_shows_count'] = upcoming_shows.count()

  return render_template('pages/show_artist.html', artist=artist_dict)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)

  if form.validate():
    error_add_new_artist = 'No_error'

    try:
      data_artist = {}

      name = request.form['name']
      city = request.form['city']
      phone = request.form.get('phone') or None
      facebook_link = request.form.get('facebook_link') or None
      website_link = request.form.get('website_link') or None
      seeking_description = request.form.get('seeking_description') or None
      seeking_venue = request.form.get('seeking_venue') or None
      image_link = request.form.get('image_link') or None


      if seeking_venue is None:
        seeking_venue = False
      else:
        seeking_venue = True

      # get state object
      state = request.form.get('state')
      artist_state = State.query.filter_by(abbreviation=state).first_or_404()

      # new artist
      new_artist = Artist(name=name, city=city, phone=phone, facebook_link=facebook_link, website_link=website_link,
                    seeking_description=seeking_description, seeking_venue=seeking_venue, image_link=image_link,
                    state_fk=artist_state.id)

      # save for use after commit
      data_artist['name']= new_artist.name
      
      db.session.add(new_artist)
      db.session.commit()
      
    except:
      error_add_new_artist = 'Error_db_add'
      db.session.rollback()
      
    finally:
      db.session.close()
  else:
      error_add_new_artist = 'Error_form'
  
  # error flash mensages
  if error_add_new_artist == 'No_error':
    flash('Artist ' + data_artist['name'] + ' was successfully added!')
  elif error_add_new_artist == 'Error_db_add':
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be added.')
  elif error_add_new_artist == 'Error_form':
    flash('Error, Invalid Form!')
    print(form.errors)
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows = Shows.query.all()
  data_shows = []
  for show in shows:
    dict_show = {
    "venue_id" : show.venue.id,
    "venue_name" :  show.venue.name,
    "artist_id": show.artist.id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time" : show.start_time.isoformat()
    }
    data_shows.append(dict_show)

  return render_template('pages/shows.html', shows=data_shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)

  if form.validate():
    error_add_new_show = 'No_error'

    try:
      venue_id = request.form['venue_id']
      artist_id = request.form['artist_id']
      start_time = request.form['start_time']
      venue = Venue.query.get_or_404(venue_id)
      artist = Artist.query.get_or_404(artist_id)
      start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

      # new show
      new_show = Shows(artist=artist, venue=venue, start_time=start_time)
      db.session.add(new_show)            
      db.session.commit()
      
    except:
      error_add_new_show = 'Error_db_add'
      db.session.rollback()
      print(sys.exc_info())
      
    finally:
      db.session.close()
  else:
      error_add_new_show = 'Error_form'
  
  # error flash mensages
  if error_add_new_show == 'No_error':
    flash('The Show was successfully added!')
  elif error_add_new_show == 'Error_db_add':
    flash('An error occurred. The Show could not be added.')
  elif error_add_new_show == 'Error_form':
    flash('Error, Invalid Form!')
    print(form.errors)

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
