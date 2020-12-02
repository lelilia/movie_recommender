from decouple import config
import requests
import gzip
import pandas as pd
import urllib

# https://www.omdbapi.com/?t=heat&apikey=apikeyhere

# 'https://datasets.imdbws.com/title.basics.tsv.gz'

dataurl = 'https://datasets.imdbws.com/title.basics.tsv.gz'


urllib.request.urlretrieve (dataurl, "data/title.basics.tsv.gz")

with gzip.open('data/title.basics.tsv.gz') as f:
    movies = pd.read_csv(f, sep='\t', chunksize=5000)

print(movies.head())

movies.to_csv('data/full_movie_list.csv')



baseurl = 'https://www.omdbapi.com/'
api_key = config('OMDB_API')


