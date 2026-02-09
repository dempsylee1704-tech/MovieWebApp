from models import db, User, Movie

class DataManager:
    def _commit(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Database commit failed: {e}")


    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        self._commit()
        return new_user

    def get_users(self):
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies

    def add_movie(self, movie):
        db.session.add(movie)
        self._commit()
        return movie

    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie is None:
            raise ValueError("Movie not found")

        movie.name = new_title
        self._commit()
        return movie

    def delete_movie(self, movie_id):
        deleted_movie = Movie.query.filter_by(id=movie_id).first()
        if deleted_movie is None:
            raise ValueError
        else:
            db.session.delete(deleted_movie)
            self._commit()
