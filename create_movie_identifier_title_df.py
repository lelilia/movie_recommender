#
import pandas as pd

#
movies = pd.read_csv('data/movies.csv')

#
movie_title_and_identifier = movies.iloc[:,0:2]

#
movie_title_and_identifier.to_csv('data/movie_title_and_identifier.csv')
