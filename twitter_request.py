import requests

from twitter_credentials import bearer_token_v2

QUERY = "query="
TWEET_FIELDS = "tweet.fields=geo"
NEXT_TOKEN = "next_token="
EXPANSIONS = "expansions=geo.place_id"
PLACE_FIELDS = "place.fields=geo,contained_within"
MAX_RESULTS = "max_results="


def twitter_embed_request(tweet_id):
    """
    A function that makes a request for the embed json of a tweet specified by id
    :param tweet_id: the id of the tweets we want to embed
    :return: a json, more about the json format here: https://developer.twitter.com/en/docs/twitter-for-websites/timelines/guides/oembed-api
    """
    tweet_url = "https://twitter.com/random/status/" + str(tweet_id)
    url = "https://publish.twitter.com/oembed?theme=dark&url=" + tweet_url
    response = requests.request("GET", url)
    return response.json()


def get_tweet_by_id(tweet_id):
    """
    A function that makes a Twitter request for a tweet specified by id
    :param tweet_id: the id of the tweets we want to search for
    :return: a Tweet object, more about this here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    """
    url = "https://api.twitter.com/2/tweets?ids={}&{}&{}&{}".format(tweet_id, TWEET_FIELDS, EXPANSIONS, PLACE_FIELDS)
    response = requests.request("GET", url, headers=TwitterRequest.build_headers())
    return response.json()


class TwitterRequest:
    """
    A class that represents the Recent search Twitter request for a specified hashtag
    Attributes
    ----------
    hashtag:
        the hashtag we want to search for
    max_results:
        the maximum number of results received per request
    headers_v2:
        the authentication header required for the requests

    Methods
    -------
    build_url(next_token=None):
        builds and returns the url string of the request
    send_request(next_token=None):
        sends the Twitter request and returns the response
    build_headers():
        builds and returns the headers required for the request
    """

    def __init__(self, hashtag=None, max_results=100):
        """

        :param hashtag: the hashtag specified by the user
        :param max_results: the maximum number of results received per request
        """
        self.hashtag = hashtag
        self.max_results = max_results
        self.headers_v2 = self.build_headers()

    def build_url(self, next_token=None):
        """
        A function that builds the request url
        :param next_token: a token for the next page of results
        :return: a string that represents the request url
        """
        query = QUERY + (self.hashtag if self.hashtag is not None else 'hello')
        max_results = MAX_RESULTS + str(self.max_results)
        url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}&{}&{}".format(
            query, TWEET_FIELDS, EXPANSIONS, PLACE_FIELDS, max_results
        )
        if next_token is not None:
            url = url + "&{}".format(NEXT_TOKEN + next_token)
        return url

    def send_request(self, next_token=None):
        """
        A function that sends a GET request at the specified url and returns the response
        :param next_token: next_token: a token for the next page of results
        :return: a json response
        """
        response = requests.request("GET", self.build_url(next_token), headers=self.headers_v2)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    @staticmethod
    def build_headers():
        """
        A function that builds the headers required for the requests
        :return: a dictionary {"Authorization" : "Bearer <bearer token>"}
        """
        headers_v2 = {"Authorization": "Bearer " + bearer_token_v2}
        return headers_v2
