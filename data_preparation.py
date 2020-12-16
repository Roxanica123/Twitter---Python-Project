from twitter_request import TwitterRequest
from user_input import escape_hashtag_sign

MAX_REQUESTS = 100


def get_recent_tweets_with_available_location(hashtag=None, wanted_results=10):
    twitter = TwitterRequest(hashtag, wanted_results * 10 if wanted_results * 10 < 100 else 100)
    tweets_with_available_location = []
    places = []
    number_of_requests = 1
    next_token = None
    while len(tweets_with_available_location) < wanted_results and number_of_requests < MAX_REQUESTS:
        response = twitter.send_request(next_token)
        data = response["data"]
        meta = response["meta"]
        for tweet in data:
            if tweet.get("geo") is not None and len(tweets_with_available_location) < wanted_results:
                tweets_with_available_location.append(tweet)
        number_of_requests += 1
        if response.get("includes") is not None and response["includes"].get("places") is not None:
            places = places + response["includes"]["places"]
        if meta.get("next_token") is not None:
            next_token = meta["next_token"]
        else:
            break
    if len(tweets_with_available_location) == 0:
        return get_recent_tweets_with_available_location(escape_hashtag_sign('#oops'))
    return extract_coordinates_from_tweets_info(tweets_with_available_location, places)


def calculate_coordinates(place):
    bbox = place["geo"]["bbox"]
    return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]


def find_tweet_place_in_places_list(tweet, places):
    place_id = tweet["geo"]["place_id"]
    return next(filter(lambda current_place: current_place["id"] == place_id, places))


def extract_coordinates_from_tweets_info(tweets, places):
    tweets_with_extracted_location = []
    for tweet in tweets:
        if tweet["geo"].get("coordinates") is not None:
            coordinates = tweet["geo"]["coordinates"]["coordinates"]
        else:
            place = find_tweet_place_in_places_list(tweet, places)
            coordinates = calculate_coordinates(place)
        tweet_with_extracted_location = {"id": tweet["id"], "text": tweet["text"], "coordinates": coordinates}
        tweets_with_extracted_location.append(tweet_with_extracted_location)
    return tweets_with_extracted_location
