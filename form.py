import bs4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class HashtagForm(FlaskForm):
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    wanted_results = IntegerField('Wanted Results', validators=[DataRequired()])
    submit = SubmitField('Show me!')


def add_form_to_map(map_string_representation):
    soup = bs4.BeautifulSoup(map_string_representation)

    form_container = soup.new_tag("form-container")
    form_tag = soup.new_tag("form", action="", method="post")
    form_tag.string = "{{ form.hidden_tag() }}"

    hashtag_tag = soup.new_tag("hashtag-container")
    hashtag_label_tag = soup.new_tag("hashtag-label")
    hashtag_label_tag.string = "{{ form.hashtag.label }}"
    hashtag_field_tag = soup.new_tag("hashtag-field")
    hashtag_field_tag.string = "{{ form.hashtag(size=32) }}"
    hashtag_tag.append(hashtag_label_tag)
    hashtag_tag.append(hashtag_field_tag)

    wanted_results_tag = soup.new_tag("wanted_results-container")
    wanted_results_label_tag = soup.new_tag("wanted-results-label")
    wanted_results_label_tag.string = "{{ form.wanted_results.label }}"
    wanted_results_field_tag = soup.new_tag("wanted-results-field")
    wanted_results_field_tag.string = "{{ form.wanted_results(size=32) }}"
    wanted_results_tag.append(wanted_results_label_tag)
    wanted_results_tag.append(wanted_results_field_tag)

    submit_tag = soup.new_tag("submit")
    submit_tag.string = "{{ form.submit() }}"

    form_tag.append(hashtag_tag)
    form_tag.append(wanted_results_tag)
    form_tag.append(submit_tag)
    form_container.append(form_tag)
    soup.body.append(form_container)
    return str(soup)
