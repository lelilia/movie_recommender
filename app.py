from flask import Flask, render_template, request, render_template_string

from functions import get_all_movie_names
from ml_models import dummy_recommendation

app = Flask(__name__)


@app.route('/')
def index():
    all_movies = get_all_movie_names()
    print(len(all_movies))
    return render_template("index.html", all_movies=all_movies)

@app.route("/recommender")
def recommend():
    result = dummy_recommendation(5)
    user_input = dict(request.args)


    return render_template("recommendations.html", user_input=user_input, result=result)

if __name__ == '__main__':
    app.run(debug=True)

