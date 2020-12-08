#
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import random
import time

from sklearn.metrics.pairwise import cosine_similarity

#
movies = pd.read_csv('data/initial_list.csv', index_col=0)
identifier_df = pd.read_csv('data/movie_title_and_identifier.csv', index_col=0)

#
def cosine_sim(data=movies,
               user_rating={'Toy Story (1995)': 5, 'Heat (1995)': 1},
               identifier_df=identifier_df,
               user_name='Yuki', n_movies=10):
    
    # fill NaN's
    data = data.apply(lambda x: x.fillna(x.mean(), axis=0))
    #data = data.fillna(0)
    
    # convert movie names into movie id's
    identifier_list = []

    for i in range(len(user_rating)):
        current_key = list(user_rating.keys())[i]
        current_val = str(int(identifier_df.loc[identifier_df['title'] == current_key, 'movieId'].values))
        identifier_list.append(current_val)

    ratings = list(user_rating.values())
    user_input_converted = dict(zip(identifier_list, ratings))
    
    # new user data frame
    user_df = pd.DataFrame(user_input_converted, index=[user_name], columns=data.columns)
    
    # fill NaN's of user w/ zeros for unseen movies
    user_df = user_df.fillna(0)
    
    # add new user to 
    data.loc[len(data.index)+1] = user_df.loc[user_name]
    
    # store active user id
    active_user = len(data.index)
    
    # compute cosine similarity on users
    cs = cosine_similarity(data)
    
    #
    cs_df = pd.DataFrame(cs)
    
    # increment index by 1
    cs_df.index += 1
    
    #
    cs_index_list = cs_df.index.values.tolist()
    
    # rename columns so that index and columns has same names (= id's)
    cs_df.columns = cs_index_list
    
    #
    largest_df = cs_df.nlargest(3, cs_df.columns[active_user-1])
    
    #
    largest_list = largest_df.index.values.tolist()
    
    #
    top_similiarity = largest_df[largest_list]
    
    #
    data_transposed = data.T
    
    #
    top_data_df = data_transposed[largest_list]
    
    #
    unseen_movies = data.T[data.T[active_user].values == 0].index
    
    #
    pred_ratings = []
    for movie in unseen_movies: 
        other_users = top_data_df.columns[top_data_df.loc[movie] > 0]
        # logic to select most similar user, e.g. top3, threshold,...
        # prediction of rating (active users): weighted average of ratings of closest neighbours
        # sum(similarity*rating)/sum(similarity)  OR sum(ratings/no.users)
        nominator = 0
        denominator = 0
        for u in other_users:
            rating = top_data_df[u][top_data_df.index == movie].values[0]
            sim = top_similiarity[u][active_user]
            nominator += (sim*rating)
            denominator += sim
        pred_rating = nominator/denominator
        pred_ratings.append((movie, pred_rating))
        
    # get highest rating value
    highest_rating = max(pred_ratings, key=itemgetter(1))[1]
    
    # get all ratings which are equal to highest rating values
    highest_rating_list = list(filter(lambda x:highest_rating in x, pred_ratings))
    
    # sample a certain number of entries of the list
    top = random.sample(highest_rating_list, n_movies)
    
    # convert to list
    movie_id_list = [sub[0] for sub in top]
    
    # convert each item of list from str to int
    movie_id_list = list(map(int, movie_id_list))
    
    # 
    movie_df = identifier_df.set_index('movieId')
    
    #
    movie_title_ranking = list(movie_df['title'].loc[movie_id_list].values)
    
    return movie_title_ranking


"""
t0 = time.time()
results = cosine_sim(data=movies,
               user_rating={'Toy Story (1995)': 4, 'Jumanji (1995)': 5, 'Lion King, The (1994)': 4},
               identifier_df=identifier_df,
               user_name='Yuki',
          n_movies=15)
print(results)
time_diff = time.time() - t0
print(time_diff)
"""

    