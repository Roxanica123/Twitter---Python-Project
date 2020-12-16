from flask import Flask, redirect
from flask import request, render_template_string

from data_preparation import get_recent_tweets_with_available_location
from form import HashtagForm, add_form_to_map
from map import Map
from user_input import unescape_hashtag, assure_hashtag_sign_existence, check_hashtag_validity, \
    check_wanted_results_validity, escape_hashtag_sign

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-secret-key'


@app.route('/', methods=['GET', 'POST'])
def get_hashtag():
    form = HashtagForm()
    if form.validate_on_submit():
        return redirect('?hashtag={}&wanted_results={}'.format(form.hashtag.data, form.wanted_results.data))

    hashtag = assure_hashtag_sign_existence(unescape_hashtag(request.args.get('hashtag')))
    wanted_results = request.args.get('wanted_results')

    if hashtag is not None and check_hashtag_validity(hashtag) and check_wanted_results_validity(wanted_results):
        results = get_recent_tweets_with_available_location(escape_hashtag_sign(hashtag), int(wanted_results))
    else:
        results = get_recent_tweets_with_available_location()
    my_map = Map(results)
    map_string_representation = my_map.get_html_string_representation()
    map_string_representation = add_form_to_map(map_string_representation)
    return render_template_string(map_string_representation, form=form)
