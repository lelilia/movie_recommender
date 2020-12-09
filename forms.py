from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class InitialMovieRatingForm(FlaskForm):
    movie_best = StringField('Best Movie', validators=[DataRequired()], render_kw={"placeholder": "your favorite movie", "class": "form-control form-control-sm"})
    rating_best = RadioField(choices=[1,2,3,4,5], default=5)
    movie_worst = StringField('Worst Movie', validators=[DataRequired()], render_kw={"placeholder": "your least favorite movie", "class": "form-control form-control-sm"})
    rating_worst = RadioField(choices=[1,2,3,4,5], default=1)
    submit = SubmitField('Recommend')