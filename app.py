import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db,db_drop_create, setup_db, Actor, Movie, Show
from config import pagination

ROWS_PER_PAGE = pagination['example']
def paginate_results(request,selection):
    page=request.args.get('page', 1, type=int)
    start=(page-1)*ROWS_PER_PAGE
    end=start+ROWS_PER_PAGE
    rows=[row.format() for row in selection]
    current_rows=rows[start:end]
    return current_rows

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  
  #endpoints of actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def retrieve_actors():
        selection = Actor.query.all()
        actors = paginate_results(request, selection)
        if len(actors)==0:
            abort(404)
        return jsonify({
            'success':True,
            'actors':actors
        })
  
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(payload):
    body = request.get_json()
    if not body:
          abort(400)
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', 'Other')
    if not name:
      abort(422)
    if not age:
      abort(422)

    add_actor = (Actor(
          name = name, 
          age = age,
          gender = gender
          ))
    add_actor.insert()

    return jsonify({
      'success': True,
      'created': add_actor.id
    })

  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actors(payload, actor_id):
    body = request.get_json()
    if not actor_id:
      abort(400)
    if not body:
      abort(400)

    update_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not update_actor:
      abort(404)
    name = body.get('name', update_actor.name)
    age = body.get('age', update_actor.age)
    gender = body.get('gender', update_actor.gender)

    update_actor.name = name
    update_actor.age = age
    update_actor.gender = gender
    update_actor.update()
    return jsonify({
      'success': True,
      'updated': update_actor.id,
      'actor' : [update_actor.format()]
    })

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):
    if not actor_id:
      abort(400)
    delete_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if not delete_actor:
        abort(404)
    delete_actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor_id
    })

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    selection = Movie.query.all()
    movies = paginate_results(request, selection)
    if len(movies) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'movies': movies
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(payload):
    body = request.get_json()
    if not body:
          abort(400)
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    if not title:
      abort(422)

    if not release_date:
      abort(422)
    add_movie = (Movie(
          title = title, 
          release_date = release_date
          ))
    add_movie.insert()

    return jsonify({
      'success': True,
      'created': add_movie.id
    })

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movies(payload, movie_id):
    body = request.get_json()
    if not movie_id:
      abort(400)
    if not body:
      abort(400)
    movie_update = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movie_update:
      abort(404)

    title = body.get('title', movie_update.title)
    release_date = body.get('release_date', movie_update.release_date)
    movie_update.title = title
    movie_update.release_date = release_date
    movie_update.update()

    return jsonify({
      'success': True,
      'edited': movie_update.id,
      'movie' : [movie_update.format()]
    })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, movie_id):
    if not movie_id:
      abort(400)
  
    delete_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if not delete_movie:
        abort(404)
    delete_movie.delete()
    
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

  
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            'success': False,
            'error':422,
            'message':'unprocessable'
        }), 422
    
  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)