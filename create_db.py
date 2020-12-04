import pandas as pd
import re
from app import db
from models import Users, Movies

db.create_all()

movies = pd.read_csv('data/ml-latest-small/movies.csv')
links = pd.read_csv('data/ml-latest-small/links.csv')
ratings = pd.read_csv('data/ml-latest-small/ratings.csv')

movies = pd.merge(movies, links, on='movieId')

movies['title'] = movies['title'].str.replace(' $', '', regex=True)
movies['year'] = movies['title'].str[-5:-1]
movies['title'] = movies['title'].str[:-7]
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
del movies['tmdbId']
movies.columns = ['id','title','genres','imdb_id','year']
ratings.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
movies.set_index('id', inplace=True)

# print(movies.head())
# print(ratings.head())
# movies.to_csv('data/movietable.csv')
ratings.to_csv('data/ratingstable.csv')


# for i in movies.itertuples():
#     exists = Movies.query.filter_by(id=i.movieId).first()
#     if exists == None:
#         movie = Movies(id=i.movieId, imdb_id=i.imdbId, title=i.title, year=i.year, genres=i.genres)
#         db.session.add(movie)
#         db.session.commit()

# for i in ratings.itertuples():
#     exists = Users.query.filter_by(id=i.userId).first()
#     if exists == None:
#         user = Users(id=i.userId, rating=i.rating, timestamp=i.timestamp, movie_id=i.movieId)
#         db.session.add(user)
#         db.session.commit()


