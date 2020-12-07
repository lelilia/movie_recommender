from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),
        nullable=False)
    movie = db.relationship('Movies',backref=db.backref('movies', lazy=True))
    rating = db.Column(db.Numeric, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.user_id} rated movie {self.movie.title} with {self.rating} at {self.timestamp}>'

class User(db.Model):
    id = db.Column(db.Integer, db.Sequence('user_id_seq', start=1001, increment=1), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rated = db.relationship('Ratings', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'