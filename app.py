from flask import Flask, render_template, request, render_template_string, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from functions import get_all_movie_names
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from app.forms import InitialMovieRatingForm, LoginForm
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

# from nmf_recommender import nmf_recommender

@app.route('/', methods=['GET', 'POST'])
def index():
    all_movies = get_all_movie_names()
    form = InitialMovieRatingForm()
    if form.validate_on_submit():
        flash(f'Your rating is: {form.movie_best.data}: {form.rating_best.data}, {form.movie_worst.data}: {form.rating_worst.data}')

        return redirect(url_for('recommend'))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    app.run(debug=True)
