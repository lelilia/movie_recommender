#
import pandas as pd
import numpy as np
from operator import itemgetter
import random
import time
import pytest

from sklearn.metrics.pairwise import cosine_similarity

from cosine_similarity import cosine_sim

#
movies = pd.read_csv('data/initial_list.csv', index_col=0)
identifier_df = pd.read_csv('data/movie_title_and_identifier.csv', index_col=0)

#
def test_output_type():

    result = cosine_sim(data=movies,
               user_rating={'Toy Story (1995)': 5, 'Heat (1995)': 1},
               identifier_df=identifier_df,
               user_name='Yuki', n_movies=10)

    assert type(result) == type(list())

