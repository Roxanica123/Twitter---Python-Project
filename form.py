import bs4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HashtagForm(FlaskForm):
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    wanted_results = IntegerField('Wanted Results', validators=[DataRequired()])
    submit = SubmitField('Show me!')


def add_form_to_map(map_string_representation):
    soup = bs4.BeautifulSoup(map_string_representation, features="html.parser")

    form_soup = bs4.BeautifulSoup(open("./static/form.html", "r").read(), features="html.parser")

    link_tag = soup.new_tag("link", rel="stylesheet", href="/static/form.css")
    soup.head.append(link_tag)
    soup.body.append(form_soup)
    return str(soup)
