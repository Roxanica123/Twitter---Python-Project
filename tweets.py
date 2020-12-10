import json

from twitter_request import TwitterRequest

MAX_REQUESTS = 100


def get_recent_tweets_with_available_location(hashtag, wanted_results):
    twitter = TwitterRequest(hashtag, wanted_results)
    tweets_with_available_location = []
    number_of_requests = 1
    next_token = None
    while len(tweets_with_available_location) < wanted_results and number_of_requests < MAX_REQUESTS:
        response = twitter.send_request(next_token)
        data = response["data"]
        meta = response["meta"]
        for tweet in data:
            if tweet.get("geo") is not None and len(tweets_with_available_location) < wanted_results:
                tweets_with_available_location.append(tweet)
        next_token = meta["next_token"]
        number_of_requests += 1
    print(tweets_with_available_location)
