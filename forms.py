from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class InitialMovieRatingForm(FlaskForm):
    movie_best = StringField('Best Movie', validators=[DataRequired()])
    rating_best = RadioField(choices=[1,2,3,4,5], default=5)
    movie_worst = StringField('Worst Movie', validators=[DataRequired()])
    rating_worst = RadioField(choices=[1,2,3,4,5], default=1)
    submit = SubmitField('Recommend')