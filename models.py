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
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'),
        nullable=False)
    movie = db.relationship('Movies',backref=db.backref('movies', lazy=True))
    rating = db.Column(db.Numeric, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.user_id} rated movie {self.movie.title} with {self.rating} at {self.timestamp}>'

