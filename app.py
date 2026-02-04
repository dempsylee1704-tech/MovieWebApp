from flask import Flask, render_template, request, redirect, url_for
from api.omdb_api import get_request_from_api
from data_manager import DataManager
from models import db, Movie, User
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form["name"]
    data_manager.create_user(name)
    return redirect(url_for('home'))



@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user=user)



@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form['title'].strip()

    info = get_request_from_api(title)
    if info is None:
        return redirect(url_for('get_movies', user_id=user_id))

    movie = Movie(
        name=info["title"],
        year=info["year"],
        director=info["director"],
        poster_url=info["poster_url"],
        user_id=user_id
    )

    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form["title"]
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_movies', user_id=user_id))



@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()