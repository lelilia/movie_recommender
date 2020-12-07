from flask import Flask, render_template, request, render_template_string
from flask_bootstrap import Bootstrap
from functions import get_all_movie_names

from nmf_recommender import nmf_recommender
from forms import InitialMovieRatingForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    all_movies = get_all_movie_names()
    form = InitialMovieRatingForm()
    if form.validate_on_submit():
        flash(f'Your rating is: {form.movie_best.data}: {form.rating_best.data}, {form.movie_worst.data}: {form.rating_worst.data}')

        return redirect(url_for('recommendations'))

    return render_template("index.html", all_movies=all_movies, form=form)

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

