from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app.models import Users, Movies

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InitialMovieRatingForm(FlaskForm):
    movie_best = StringField('Best Movie', validators=[DataRequired()], render_kw={'list': 'movie-list', 'placeholder': 'your favorite movie', 'class': 'form-control form-control-sm'})
    rating_best = RadioField(choices=[1,2,3,4,5], default=5)
    movie_worst = StringField('Worst Movie', validators=[DataRequired()], render_kw={'list': 'movie-list','placeholder': 'your least favorite movie', 'class': 'form-control form-control-sm'})
    rating_worst = RadioField(choices=[1,2,3,4,5], default=1)
    submit = SubmitField('Recommend',render_kw={"class": "btn btn-default"})

    def validate_movie_best(self, movie_best):
        movie = Movies.query.filter_by(title=movie_best.data).first()
        if movie is None:
            raise ValidationError('Please choose a movie that is in the database')

    def validate_movie_worst(self, movie_worst):
        movie = Movies.query.filter_by(title=movie_worst.data).first()
        if movie is None:
            raise ValidationError('Please choose a movie that is in the database')

