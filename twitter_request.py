import requests

from twitter_credentials import bearer_token_v2

QUERY = "query="
TWEET_FIELDS = "tweet.fields=geo"
NEXT_TOKEN = "next_token="
EXPANSIONS = "expansions=geo.place_id"
PLACE_FIELDS = "place.fields=geo,contained_within"
MAX_RESULTS = "max_results="


def twitter_embed_request(tweet_id):
    tweet_url = "https://twitter.com/random/status/" + str(tweet_id)
    url = "https://publish.twitter.com/oembed?theme=dark&url=" + tweet_url
    response = requests.request("GET", url)
    return response.json()


def get_tweet_by_id(tweet_id):
    url = "https://api.twitter.com/2/tweets?ids={}&{}&{}&{}".format(tweet_id, TWEET_FIELDS, EXPANSIONS, PLACE_FIELDS)
    response = requests.request("GET", url, headers=TwitterRequest.build_headers())
    return response.json()


class TwitterRequest:
    def __init__(self, hashtag=None, max_results=100):
        self.hashtag = hashtag
        self.max_results = max_results
        self.headers_v2 = self.build_headers()

    def build_url(self, next_token=None):
        query = QUERY + (self.hashtag if self.hashtag is not None else 'hello')
        max_results = MAX_RESULTS + str(self.max_results)
        url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}&{}&{}".format(
            query, TWEET_FIELDS, EXPANSIONS, PLACE_FIELDS, max_results
        )
        if next_token is not None:
            url = url + "&{}".format(NEXT_TOKEN + next_token)
        return url

    def send_request(self, next_token=None):
        response = requests.request("GET", self.build_url(next_token), headers=self.headers_v2)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    @staticmethod
    def build_headers():
        headers_v2 = {"Authorization": "Bearer " + bearer_token_v2}
        return headers_v2
