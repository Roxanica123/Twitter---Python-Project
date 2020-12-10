from data_preparation import get_recent_tweets_with_available_location
from user_input import get_input_hashtag

WANTED_RESULTS = 2


def main():
    hashtag = get_input_hashtag()
    print(get_recent_tweets_with_available_location(hashtag, WANTED_RESULTS))


if __name__ == "__main__":
    main()
