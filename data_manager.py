from models import db, User, Movie

class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie is None:
            raise ValueError("Movie not found")

        movie.name = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        deleted_movie = Movie.query.filter_by(id=movie_id).first()
        if deleted_movie is None:
            raise ValueError
        else:
            db.session.delete(deleted_movie)
            db.session.commit()
