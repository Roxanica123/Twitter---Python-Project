from flask import Flask, abort
from flask import request

from data_preparation import get_recent_tweets_with_available_location
from map import Map
from user_input import unescape_hashtag, assure_hashtag_sign_existence, check_hashtag_validity, \
    check_wanted_results_validity, escape_hashtag_sign

app = Flask(__name__)


@app.route('/tweets')
def hello_world():
    hashtag = assure_hashtag_sign_existence(unescape_hashtag(request.args.get('hashtag')))
    wanted_results = request.args.get('wanted_results')

    if hashtag is not None and check_hashtag_validity(hashtag) and check_wanted_results_validity(wanted_results):
        results = get_recent_tweets_with_available_location(escape_hashtag_sign(hashtag), int(wanted_results))
        my_map = Map(results)
        cv = my_map.get_html_string_representation()
        return cv
    abort(400)
