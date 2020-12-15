from flask import Flask, abort, redirect, render_template
from flask import request, render_template_string

from data_preparation import get_recent_tweets_with_available_location
from form import HashtagForm
from map import Map
from user_input import unescape_hashtag, assure_hashtag_sign_existence, check_hashtag_validity, \
    check_wanted_results_validity, escape_hashtag_sign

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-secret-key'


@app.route('/tweets')
def tweets():
    hashtag = assure_hashtag_sign_existence(unescape_hashtag(request.args.get('hashtag')))
    wanted_results = request.args.get('wanted_results')

    if hashtag is not None and check_hashtag_validity(hashtag) and check_wanted_results_validity(wanted_results):
        results = get_recent_tweets_with_available_location(escape_hashtag_sign(hashtag), int(wanted_results))
        my_map = Map(results)
        cv = my_map.get_html_string_representation()
        return render_template_string(cv)
    abort(400)


@app.route('/', methods=['GET', 'POST'])
def get_hashtag():
    form = HashtagForm()
    if form.validate_on_submit():
        return redirect('/tweets?hashtag={}&wanted_results={}'.format(form.hashtag.data, form.wanted_results.data))
    return render_template('form.html', form=form)
