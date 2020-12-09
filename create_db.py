import pandas as pd
import re
from app import db

from app.models import Ratings, Movies, Users

db.drop_all()
db.create_all()


path_to_files = 'data/ml-latest-small/'
engine = db.get_engine()


users = pd.DataFrame(data=range(1,611), columns=['id'])
users.to_sql('users', con=engine, index=False, if_exists='append')

movies = pd.read_csv(path_to_files + 'movies_c.csv')
links = pd.read_csv(path_to_files + 'links.csv')
movies = pd.merge(movies, links, on='movieId')

movies['title'] = movies['title'].str.replace(' $', '', regex=True)
movies['year'] = movies['title'].str[-5:-1]
movies['title'] = movies['title'].str[:-7]
del movies['tmdbId']
movies.columns = ['id', 'title', 'genres', 'imdb_id', 'year']

movies.to_sql('movies', con=engine, index=False, if_exists='append')

ratings = pd.read_csv(path_to_files + 'ratings.csv')
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
ratings = ratings.reset_index()
ratings.columns = ['id', 'user_id', 'movie_id', 'rating', 'timestamp']

ratings.to_sql('ratings', con=engine, index=False, if_exists='append')
#