#
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF

#
R = pd.read_csv('data/initial_list.csv', index_col=0)
identifier_df = pd.read_csv('data/movie_title_and_identifier.csv')

"""
innput for nmf-recommender:
movies = ['Toy Story (1995)', 'Heat (1995)']
ratings = [5, 1]
user_rating = dict(zip(movies, ratings)) 
"""


#
def nmf_recommender(data=R, 
                    user_rating=None, 
                    user_name=None, 
                    identifier_df=None,
                   ratings=None):
        
    # replace NaN's with 0
    R_imputed = R.replace(np.nan, 0)
    
    # matrix factorization
    nmf = NMF(n_components=20, max_iter=1000)
    nmf.fit(R_imputed)
    
    Q = nmf.components_
    P = nmf.transform(R_imputed)
    
    R_hat = pd.DataFrame(np.dot(P, Q), columns=R.columns, index=R.index)
    
    # convert user input
    identifier_list = []

    for i in range(len(user_rating)):
        current_key = list(user_rating.keys())[i]
        current_val = str(int(identifier_df.loc[identifier_df['title'] == current_key, 'movieId'].values))
        identifier_list.append(current_val)
    
    user_input_converted = dict(zip(identifier_list, ratings))
    
    # new user data frame
    user = pd.DataFrame(user_input_converted, index=[user_name], columns=R.columns)
    
    # fill NaN's of user
    user = user.fillna(3)
    
    user_p = nmf.transform(user)
    
    user_r = pd.DataFrame(np.dot(user_p, Q), index=[user_name], columns=R.columns)
    
    # drop movie identifiers which user has already seen
    recommend = user_r.drop(columns=user_input_converted.keys())
    
    # build data frame out of recommend columns
    not_watched_identifiers = pd.DataFrame(recommend.columns)
    not_watched_identifiers.columns = ['movieId']
    not_watched_identifiers['movieId'] = not_watched_identifiers['movieId'].astype(np.int64)
    
    # merge data frames by movieId
    merge_df = pd.merge(not_watched_identifiers, identifier_df, on='movieId', how='inner')
    
    #
    movies_not_watched_list = merge_df['title'].to_list()
    
    # convert identifiers to movie names
    recommend.columns = movies_not_watched_list
    
    # sort movie recommends
    recommend = recommend.T.sort_values(by=user_name, ascending=False)
    
    return recommend


"""
Test:

movies = ['Toy Story (1995)', 'Heat (1995)']
ratings = [5, 1]
user_rating = dict(zip(movies, ratings)) 
results = nmf_recommender(data=R, 
                user_rating=user_rating, 
                user_name='Yuki', 
                identifier_df=identifier_df,
                ratings=ratings)

print(results)
"""



