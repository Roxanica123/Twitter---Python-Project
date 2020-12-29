from twitter_request import TwitterRequest, get_tweet_by_id

MAX_REQUESTS = 100
"""The maximum number of Twitter requests that can be made for a single hashtag"""
HELLO_TWEET_ID = "1342530746838372355"
"""The tweet id for the hello tweet"""
NO_RESULTS_TWEET_ID = "1342523611614236672"
"""The tweet id for the no results tweet"""
WRONG_INPUTS_TWEET_ID = "1342542645558706181"
"""The tweet id for the wrong inputs tweet"""


def get_recent_tweets_with_available_location(hashtag=None, wanted_results=10):
    """
    A function that receives a hashtag and a number of wanted results, makes multiple Twitter requests for the specified
    hashtag and returns the most recent wanted_results tweets that contain the specified hashtag
    :param hashtag: a string representing the wanted hashtag
    :param wanted_results: the desired number of tweets with the specified hashtag
    :return: a list of dictionaries that contain "id", "text", "coordinates" of the tweets
    """
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
    """
    A function that returns a list that contains a single tweet used for user warnings visualisation
    :param hello: specifies if the tweet wanted is the hello tweet
    :param no_results: specifies if the tweet wanted is the no results tweet
    :param wrong_inputs: specifies if the tweet wanted is the wrong inputs tweet
    :return: a list that contains a single dictionary with "id", "text", "coordinates" of the tweet
    """
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
    """
    A function that calculates the middle point of a place bbox
    :param place: a Twitter place object, more about this here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    :return: a list [longitude, latitude]
    """
    bbox = place["geo"]["bbox"]
    return [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]


def find_tweet_place_in_places_list(tweet, places):
    """
    A function that matches a tweet with a place using the tweet id
    :param tweet:  a Twitter tweet object, more about this here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    :param places: a Twitter place object, more about this here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    :return: a place that has the same id as the given tweet or None if there is no such place
    """
    place_id = tweet["geo"]["place_id"]
    return next(filter(lambda current_place: current_place["id"] == place_id, places))


def extract_coordinates_from_tweets_info(tweets, places):
    """
    A function that extracts just the needed info from the Tweet and Place objects, matching the tweets and the places based on the tweet id
    :param tweets: a list of Tweet objects, more about these here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    :param places: a list of Place objects, more about these here: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    :return: a list of dictionaries with the extracted "id", "text" and "coordinates"
    """
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
