from twitter_request import TwitterRequest, get_tweet_by_id
from user_input import escape_hashtag_sign

MAX_REQUESTS = 100
HELLO_TWEET_ID = "1342530746838372355"
NO_RESULTS_TWEET_ID = "1342523611614236672"
WRONG_INPUTS_TWEET_ID = "1342542645558706181"


def get_recent_tweets_with_available_location(hashtag=None, wanted_results=10):
    twitter = TwitterRequest(hashtag, wanted_results * 10 if wanted_results * 10 < 100 else 100)
    tweets_with_available_location = []
    places = []
    number_of_requests = 1
    next_token = None
    while len(tweets_with_available_location) < wanted_results and number_of_requests < MAX_REQUESTS:
        response = twitter.send_request(next_token)
        meta = response["meta"]
        if meta["result_count"] == 0:
            break
        data = response["data"]
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
        return get_message_tweet(no_results=True)
    return extract_coordinates_from_tweets_info(tweets_with_available_location, places)


def get_message_tweet(hello=False, no_results=False, wrong_inputs=False):
    if no_results is True and hello is False and wrong_inputs is False:
        response = get_tweet_by_id(NO_RESULTS_TWEET_ID)
    elif wrong_inputs is True and hello is False:
        response = get_tweet_by_id(WRONG_INPUTS_TWEET_ID)
    else:
        response = get_tweet_by_id(HELLO_TWEET_ID)
    data = response["data"]
    tweet = [data[0]]
    place = response["includes"]["places"]
    return extract_coordinates_from_tweets_info(tweet, place)


def calculate_coordinates(place):
    bbox = place["geo"]["bbox"]
    return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]


def find_tweet_place_in_places_list(tweet, places):
    place_id = tweet["geo"]["place_id"]
    return next(filter(lambda current_place: current_place["id"] == place_id, places))


def extract_coordinates_from_tweets_info(tweets, places):
    existent = 1
    tweets_with_extracted_location = []
    for tweet in tweets:
        if tweet["geo"].get("coordinates") is not None:
            coordinates = tweet["geo"]["coordinates"]["coordinates"]
        else:
            place = find_tweet_place_in_places_list(tweet, places)
            coordinates = calculate_coordinates(place)

        if next((x for x in tweets_with_extracted_location if x["coordinates"] == coordinates), None) is not None:
            coordinates = [x + 0.00005 * existent for x in coordinates]
            existent += 1
        tweet_with_extracted_location = {"id": tweet["id"], "text": tweet["text"], "coordinates": coordinates}
        tweets_with_extracted_location.append(tweet_with_extracted_location)
    return tweets_with_extracted_location
