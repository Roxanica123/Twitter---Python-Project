from flask import Flask, redirect, render_template
from flask import request, render_template_string

from data_preparation import get_recent_tweets_with_available_location, get_message_tweet
from form import HashtagForm, add_form_to_map
from map import Map
from user_input import unescape_hashtag, assure_hashtag_sign_existence, check_hashtag_validity, \
    check_wanted_results_validity, escape_hashtag_sign

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random-secret-key'


@app.route('/', methods=['GET', 'POST'])
def get_hashtag():
    """
    A function that receives a request and returns the map html representation for that request
    :return: a string representing the html representation of the map for the given request
    """
    form = HashtagForm()
    if form.validate_on_submit():
        return redirect('?hashtag={}&wanted_results={}'.format(form.hashtag.data, form.wanted_results.data))
    hashtag = assure_hashtag_sign_existence(unescape_hashtag(request.args.get('hashtag')))
    wanted_results = request.args.get('wanted_results')

    if hashtag is not None and check_hashtag_validity(hashtag) and check_wanted_results_validity(wanted_results):
        try:
            results = get_recent_tweets_with_available_location(escape_hashtag_sign(hashtag), int(wanted_results))
        except:
            return render_template_string(open("./static/error.html").read())
    else:
        try:
            results = get_message_tweet(hello=True) if len(request.args) == 0 else get_message_tweet(wrong_inputs=True)
        except:
            return render_template_string(open("./static/error.html").read())
    my_map = Map(results)
    map_string_representation = my_map.get_html_string_representation()
    map_string_representation = add_form_to_map(map_string_representation)
    return render_template_string(map_string_representation, form=form)
