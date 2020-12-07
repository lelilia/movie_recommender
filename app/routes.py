from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.models import Movies, Ratings, User
from app.forms import InitialMovieRatingForm, LoginForm

from app.nmf import nmf_recommender

@app.route('/', methods=['GET', 'POST'])
def index():
    all_movies = Movies.query.order_by(Movies.title).all()
    form = InitialMovieRatingForm()
    if form.validate_on_submit():
        flash(f'Your rating is: {form.movie_best.data}: {form.rating_best.data}, {form.movie_worst.data}: {form.rating_worst.data}')
        m_id_best = Movies.query.filter_by(title=form.movie_best.data).first().id
        m_id_worst = Movies.query.filter_by(title=form.movie_worst.data).first().id
        nmf_result = {m_id_best: form.rating_best.data, m_id_worst: form.rating_worst.data}
        print('------------------------')
        print(nmf_result)
        return redirect(url_for('rec', rec_list = nmf_result))

    return render_template("index1.html", all_movies=all_movies, form=form)

@app.route('/rec')
def rec():
    print(rec_list)
    result = []
    for r in rec_list:
        m = Movies.query.get(r)
        result.append(m.title)
    return render_template('recommendations.html', result=result)

@app.route("/recommender")
def recommend():
    # result = dummy_recommendation(5)
    user_input_raw = dict(request.args)

    # TODO hard coded! needs to change
    movies = [user_input_raw['fav_movie'], user_input_raw['worst_movie']]
    movie_ids = []
    for m in movies:
        m_id = Movies.query.filter_by(title=m).first_or_404()
        movie_ids.append(m_id.id)
    ratings = [5, 1]
    user_input = dict(zip(movie_ids, ratings))
    print(user_input)
    print(movie_ids)
    nmf_result = nmf_recommender(user_rating=user_input)
    result = []
    for r in nmf_result:

        m = Movies.query.get(r)

        result.append(m.title)

    return render_template("recommendations.html", user_input=user_input, result=result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
