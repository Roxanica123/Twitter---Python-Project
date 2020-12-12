from data_preparation import get_recent_tweets_with_available_location
from map import Map
from user_input import get_input_hashtag

WANTED_RESULTS = 10


def main():
    hashtag = get_input_hashtag()
    results = get_recent_tweets_with_available_location(hashtag, WANTED_RESULTS)
    my_map = Map(results)
    my_map.save_map("index.html")


if __name__ == "__main__":
    main()
