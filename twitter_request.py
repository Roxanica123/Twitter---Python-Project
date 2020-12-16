import requests

from twitter_credentials import bearer_token_v2

QUERY = "query="
TWEET_FIELDS = "tweet.fields="
NEXT_TOKEN = "next_token="
EXPANSIONS = "expansions="
PLACE_FIELDS = "place.fields="
MAX_RESULTS = "max_results="


class TwitterRequest:
    def __init__(self, hashtag=None, max_results=100):
        self.hashtag = hashtag
        self.max_results = max_results
        self.headers_v2 = self.build_headers()

    def build_url(self, next_token=None):
        query = QUERY + (self.hashtag if self.hashtag is not None else 'hello')
        tweet_fields = TWEET_FIELDS + "geo"
        expansions = EXPANSIONS + "geo.place_id"
        place_fields = PLACE_FIELDS + "geo,contained_within"
        max_results = MAX_RESULTS + str(self.max_results)
        url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}&{}&{}".format(
            query, tweet_fields, expansions, place_fields, max_results
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
