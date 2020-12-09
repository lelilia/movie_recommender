from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    genres = db.Column(db.Text)
    imdb_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<Movie {self.id} - {self.title}>'

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),
        nullable=False)
    movie = db.relationship('Movies',backref=db.backref('got_rated', lazy=True))
    user = db.relationship('Users', backref=db.backref('rated', lazy=True))
    rating = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.user_id} rated movie {self.movie.title} with {self.rating} at {self.timestamp}>'

    def update_rating(self, rating):
        self.rating = rating
        self.timestamp = datetime.utcnow()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #rated = db.relationship('Ratings', backref='users', lazy='dynamic')
    rantings_dict = {}

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def rated_movies(self):
        pass
