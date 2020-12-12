import re
import sys
from urllib.parse import quote, unquote

MAX_WANTED_RESULTS = 1000


def check_hashtag_validity(hashtag):
    match = re.fullmatch(r"#[a-zA-Z]+\d*([a-zA-Z]*\d*)*", hashtag)
    return False if match is None else True


def check_wanted_results_validity(wanted_results):
    try:
        wanted_results = int(wanted_results)
        if wanted_results < MAX_WANTED_RESULTS:
            return True
        else:
            return False
    except:
        return False


def assure_hashtag_sign_existence(hashtag):
    return hashtag if (hashtag is None or (len(hashtag) > 0 and hashtag[0] == '#')) else '#' + hashtag


def escape_hashtag_sign(hashtag):
    return quote(hashtag)


def unescape_hashtag(hashtag):
    return unquote(hashtag) if hashtag is not None else None


def get_input_hashtag():
    if len(sys.argv) > 1:
        hashtag = sys.argv[1]
    else:
        hashtag = input("Hey hey! Please give me the hashtag you want.\n")
    hashtag = assure_hashtag_sign_existence(hashtag)
    while check_hashtag_validity(hashtag) is False:
        hashtag = assure_hashtag_sign_existence(input("Ooops, your hashtag is not valid, try again.\n"))
    return escape_hashtag_sign(hashtag)
