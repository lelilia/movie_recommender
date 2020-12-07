from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

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
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InitialMovieRatingForm(FlaskForm):
    movie_best = StringField('Best Movie', validators=[DataRequired()])
    rating_best = RadioField(choices=[1,2,3,4,5], default=5)
    movie_worst = StringField('Worst Movie', validators=[DataRequired()])
    rating_worst = RadioField(choices=[1,2,3,4,5], default=1)
    submit = SubmitField('Recommend')