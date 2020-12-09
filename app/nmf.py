import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import random
import pickle
import os

from app import db
from app.models import Ratings, Users

def get_model(R, pkl_file='app/nmf.pkl'):
    ''' either load the model from file or train a new model'''
    if os.path.exists(pkl_file):
        print('Loading Model from File')
        with open(pkl_file, 'rb') as file:
            nmf = pickle.load(file)
    else:
        nmf = NMF(n_components=20, max_iter=1000)
        nmf.fit(R)
        with open(pkl_file, 'wb') as file:
            
            pickle.dump(nmf, file)
    return nmf


engine = db.get_engine()
R = pd.read_sql_query('SELECT user_id, movie_id, rating FROM ratings', con=engine)
R = R.pivot(index='user_id', columns='movie_id', values='rating')


average_movie_rating = R.mean().mean()
R_imputed = R.fillna(average_movie_rating)
nmf = get_model(R=R_imputed)

Q = nmf.components_
P = nmf.transform(R_imputed)

R_hat = pd.DataFrame(np.dot(P,Q), columns=R.columns, index=R.index)



def nmf_recommender(user_rating = {1:5, 3:3}, user_id=99999, max_length=10):
    ''' get movie recommendation with nmf model based on favorite and least favorite movie'''

    if user_rating is None:
        user_rating = {}
        u = Users.query.get(user_id)
        print('------------------')
        print(u)
        print(u.rated)
        print('--------------------')
        for r in u.rated:
            user_rating[r.movie.id] = r.rating
        print(user_rating)
    user = pd.DataFrame(user_rating, index = [user_id], columns = R.columns)
    print(user)
    user = user.fillna(0)

    user_p = nmf.transform(user)
    user_r = pd.DataFrame(np.dot(user_p, Q), index = user.index, columns=user.columns)

    rec = user_r.drop(columns=user_rating.keys())

    rec_trans = rec.T
    rec_trans = rec_trans.sort_values(by=[user_id], ascending=False)

    rec = rec_trans[:max_length]

    return list(rec.index)

if __name__ == '__main__':
    print(nmf_recommender())