from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HashtagForm(FlaskForm):
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    wanted_results = IntegerField('Wanted Results', validators=[DataRequired()])
    submit = SubmitField('Show me!')
