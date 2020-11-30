''' Saves the data in a csv with userId as index and movieId as columns '''

import pandas as pd

ratings = pd.read_csv('data/ml-latest-small/ratings.csv')
ratings = ratings.pivot(index='userId', columns='movieId', values='rating')
ratings.to_csv('data/inital_list.csv')