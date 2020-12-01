''' Saves the data in a csv with userId as index and movieId as columns '''

import pandas as pd

ratings = pd.read_csv('data/ratings.csv')
ratings = ratings.pivot(index='userId', columns='movieId', values='rating')
ratings.to_csv('data/initial_list.csv')
