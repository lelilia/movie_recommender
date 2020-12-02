from flask import Flask, render_template, request, render_template_string

from functions import get_all_movie_names
from ml_models import dummy_recommendation

app = Flask(__name__)


@app.route('/')
def index():
    all_movies = get_all_movie_names()
    return render_template("index.html", all_movies=all_movies)

@app.route("/recommender")
def recommend():
    result = dummy_recommendation(5)
    user_input_raw = dict(request.args)
    # TODO hard coded! needs to change
    movies = [user_input_raw['fav_movie'], user_input_raw['worst_movie']]
    ratings = [5, 1]
    user_input = dict(zip(movies, ratings))


    return render_template("recommendations.html", user_input=user_input, result=result)

if __name__ == '__main__':
    app.run(debug=True)

