import pandas as pd

def get_all_movie_names():
    movies = pd.read_csv('data/ml-latest-small/movies.csv')
    all_movie_names = movies['title'].values
    return all_movie_names

if __name__ == '__main__':
    res = get_all_movie_names()
    print(res)