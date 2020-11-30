# import modules
import pandas as pd

# load files
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# merge movies and rating by movieId
df_merge = pd.merge(ratings, movies, on='movieId', how='outer')

# pivoting
p_mt = df_merge.pivot(values='rating', index=['userId'], columns=['movieId']).values
p_mt = pd.DataFrame(p_mt)
p_mt = p_mt.iloc[1:]

# get titles for column names
columns = list(movies['title'])

# set column names
p_mt.columns = columns

# store p-matrix
p_mt.to_csv('data/initial_p_matrix_complete.csv')