from flask import Flask, render_template, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from functions import get_all_movie_names
# from ml_models import dummy_recommendation
from nmf_recommender import nmf_recommender


db_url = config('DATABASE_URL')
db_pw = config('DATABASE_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_pw}@{db_url}:5432/movie-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    all_movies = get_all_movie_names()
    return render_template("index.html", all_movies=all_movies)

@app.route("/recommender")
def recommend():
    # result = dummy_recommendation(5)
    user_input_raw = dict(request.args)
    # TODO hard coded! needs to change
    movies = [user_input_raw['fav_movie'], user_input_raw['worst_movie']]
    ratings = [5, 1]
    user_input = dict(zip(movies, ratings))

    result = nmf_recommender(user_rating = user_input)

    return render_template("recommendations.html", user_input=user_input, result=result)

if __name__ == '__main__':
    app.run(debug=True)

