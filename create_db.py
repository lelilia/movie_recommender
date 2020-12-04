import pandas as pd
import re
from app import db
from models import Users, Movies

db.create_all()

movies = pd.read_csv('data/ml-latest-small/movies.csv')
links = pd.read_csv('data/ml-latest-small/links.csv')
ratings = pd.read_csv('data/ml-latest-small/ratings.csv')

movies = pd.merge(movies, links, on='movieId')

def clean(string):
    result = re.sub(r'\) $', ')', string)
    return result

movies['title'] = clean(str(movies['title']))
movies['year'] = movies['title'].str[-5:-1]
movies['title'] = movies['title'].str[:-7]
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')




for i in movies.itertuples():
    print(i)
    movie = Movies(id=i.movieId, imdb_id=i.imdbId, title=i.title, year=i.year, genres=i.genres)
    db.session.add(movie)
    db.session.commit()

for i in ratings.itertuples():
    user = Users(id=i.userId, rating=i.rating, timestamp=i.timestamp, movie_id=i.movieId)
    db.session.add(user)
    db.session.commit()


