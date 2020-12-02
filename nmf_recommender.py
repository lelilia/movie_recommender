#
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF

#
R = pd.read_csv('data/initial_list.csv', index_col=0)
identifier_df = pd.read_csv('data/movie_title_and_identifier.csv')


#
def nmf_recommender(data=R, 
                    user_rating={'Toy Story (1995)': 5, 'Heat (1995)': 1}, 
                    user_name='Yuki', 
                    identifier_df=identifier_df,
                   n_movies=10):
        
    
    # NaN imputation: mean for each column (= movie)
    # R_imputed = R.apply(lambda x: x.fillna(x.mean(), axis=0))
    
    # NaN imputation: mean for each column
    average_movie_rating = R.mean().mean()
    R_imputed = R.fillna(average_movie_rating)
    
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
    
    ratings = list(user_rating.values())
    user_input_converted = dict(zip(identifier_list, ratings))
    
    # new user data frame
    user = pd.DataFrame(user_input_converted, index=[user_name], columns=R.columns)
    
    # fill NaN's of user w/ a certain number
    user = user.fillna(3)
    
    # fill NaN's with mean of the corresponding movie
    # user = user.fillna(R.mean())
    
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
    recommend_transposed = recommend.T
    recommend_transposed['movie_ranking'] = recommend_transposed.index
    recommend_ranks = recommend_transposed.sort_values(by=user_name, ascending=False)
    ranks_list = list(recommend_ranks['movie_ranking'])[:n_movies]
    
    return ranks_list

"""
# test for Yuki
user_rating = {'Toy Story (1995)': 5, 'Garfield: The Movie (2004)': 5, 
               'Forrest Gump (1994)': 1,  'Heat (1995)': 1}
results = nmf_recommender(user_rating=user_rating, n_movies=15)
print(results)
"""