#
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import pickle
import random
import pytest
from nmf_recommender import nmf_recommender



R = pd.read_csv('data/ratings.csv')
R = R.pivot(index='userId', columns='movieId', values='rating')
R.columns = R.columns.astype(str)

identifier_df = pd.read_csv('data/movie_title_and_identifier.csv', index_col=0)

"""
def test_length():
    result_list = nmf_recommender(data=R,
                    user_rating={'Toy Story': 5, 'Heat': 1},
                    user_name='Yuki', 
                    identifier_df=identifier_df,
                   n_movies=10, pretrained=True)
    assert len(result_list) <= 50
"""
