from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.models import Users, Movies, Ratings
from app.forms import InitialMovieRatingForm, LoginForm, RegistrationForm

from app.nmf import nmf_recommender


@app.route('/', methods=['GET', 'POST'])
def index():
    # if not current_user.is_authenticated:
    #     redirect(url_for('index_without_loggin'))
    all_movies = Movies.query.order_by(Movies.title).all()
    form = InitialMovieRatingForm()
    if form.validate_on_submit():
        flash(f'Your rating is: {form.movie_best.data}: {form.rating_best.data}, {form.movie_worst.data}: {form.rating_worst.data}')

        if current_user.is_anonymous:
            u = Users.query.get(99999)
            for r in u.rated:
                db.session.delete(r)
            db.session.commit()

        if current_user.is_authenticated and current_user.id != 99999:
            u = current_user

        m_best = Movies.query.filter_by(title=form.movie_best.data).first()
        # if the user already rated this movie:
        prev_rating = Ratings.query.filter_by(movie=m_best, user=u).first()
        if prev_rating is None:
            r = Ratings(rating=form.rating_best.data, movie=m_best, user=u)
            db.session.add(r)
            db.session.commit()
        else:
            prev_rating.update_rating(form.rating_best.data)

        m_worst = Movies.query.filter_by(title=form.movie_worst.data).first()
        prev_rating = Ratings.query.filter_by(movie=m_worst, user=u).first()
        if prev_rating is None:
            r = Ratings(rating=form.rating_worst.data, movie=m_worst, user=u)
            db.session.add(r)
            db.session.commit()
        else:
            prev_rating.update_rating(form.rating_worst.data)

        return redirect(url_for('rec'))

    return render_template("index.html", title="Home Page", all_movies=all_movies, form=form)

@app.route('/rec')
def rec():
    if current_user.is_anonymous:
        u = Users.query.get(99999)

    else:
        u = current_user
    nmf_result = nmf_recommender(user_id=u.id)
    result = []
    for r in nmf_result:
        m = Movies.query.get(r)
        result.append(m.title)
    print('--------------------')
    print('RESULT')
    print(result)
    return render_template ('recommendations.html', result=result)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)