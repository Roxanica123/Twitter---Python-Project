from tweets import get_recent_tweets_with_available_location
from user_input import get_input_hashtag

WANTED_RESULTS = 5


def main():
    hashtag = get_input_hashtag()
    get_recent_tweets_with_available_location(hashtag, WANTED_RESULTS)


if __name__ == "__main__":
    main()
