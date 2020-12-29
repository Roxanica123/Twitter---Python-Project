import re
import sys
from urllib.parse import quote, unquote

MAX_WANTED_RESULTS = 1000
""" The maximum value for wanted results"""


def check_hashtag_validity(hashtag):
    """
    A function that checks if a given hashtag is valid
    :param hashtag: a string that represents a hashtag
    :return: True is the hashtag is valid, False otherwise
    """
    match = re.fullmatch(r"#[a-zA-Z]+\d*([a-zA-Z]*\d*)*", hashtag)
    return False if match is None else True


def check_wanted_results_validity(wanted_results):
    """
    A functions that checks if the wanted results is an integer and less that the maximum number of wanted results
    :param wanted_results: a number of wanted results
    :return: True if the wanted results is a number smaller than the maximum number if wanted results, False otherwise
    """
    try:
        wanted_results = int(wanted_results)
        if wanted_results < MAX_WANTED_RESULTS:
            return True
        else:
            return False
    except:
        return False


def assure_hashtag_sign_existence(hashtag):
    """
    A function that checks if a string begins with a hashtag ot not
    :param hashtag: a string
    :return: the given '#'+hashtag if there was no '#' at the beginning or hashtag otherwise
    """
    print(hashtag)
    return hashtag if (hashtag is None or (len(hashtag) > 0 and hashtag[0] == '#')) else '#' + hashtag


def escape_hashtag_sign(hashtag):
    """
    A function that escapes the hashtag sign
    :param hashtag: a string
    :return: an escaped string
    """
    return quote(hashtag)


def unescape_hashtag(hashtag):
    """
    A function that unescapes the hashtag
    :param hashtag: a string
    :return: an unescaped string
    """
    return unquote(hashtag) if hashtag is not None else None


def get_input_hashtag():
    """
    A function that gets the wanted hashtag  from the command line
    :return: a string representing an escaped hashtag
    """
    if len(sys.argv) > 1:
        hashtag = sys.argv[1]
    else:
        hashtag = input("Hey hey! Please give me the hashtag you want.\n")
    hashtag = assure_hashtag_sign_existence(hashtag)
    while check_hashtag_validity(hashtag) is False:
        hashtag = assure_hashtag_sign_existence(input("Ooops, your hashtag is not valid, try again.\n"))
    return escape_hashtag_sign(hashtag)
