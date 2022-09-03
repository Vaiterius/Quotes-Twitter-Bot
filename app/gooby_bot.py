"""A Twitter bot that tweets daily Monty Python quotes"""
import time
import logging
import random

import tweepy
import schedule
from schedule import run_pending
from better_profanity import profanity

# from . import utils, config
from app import utils, config, movie_quotes, responses
from api_wrapper import wrapper
# from movie_quotes import movie_quotes
# from responses import funny_responses, roast_responses, responses_to_profanity

# Create and configure logger.
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(filename="log.txt",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode = "w")
logger = logging.getLogger()

MAX_LENGTH = 280  # Max tweet length.


def read_last_seen_id(FILE_NAME) -> int:
    """Read latest ID from file and return it."""
    with open(FILE_NAME, "r") as file:
        last_seen_id = int(file.read().strip())
        return last_seen_id


def store_last_seen_id(FILE_NAME, last_seen_id):
    """Takes latest ID from call and store it into file."""
    with open(FILE_NAME, "w") as file:
        file.write(str(last_seen_id))
        return


def follow_followers(twitter_api):
    """Follow anyone that follows bot."""
    logger.info("Retrieving and following followers.")
    for follower in tweepy.Cursor(twitter_api.get_followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()


def tweet_monty_python(twitter_api, monty_python_api):
    """
    Tweets either:
    - A handpicked quote from a list
    - A random quote from the API
    - Random sketch dialogue from the API
    """
    choice_function = random.randint(0, 2)
    tweet = ""
    if choice_function == 0:
        tweet += random.choice(movie_quotes.movie_quotes)
    elif choice_function == 1:
        tweet += utils.tweet_random_quote(monty_python_api)
    else:
        tweet += utils.tweet_random_sketch(monty_python_api)
    
    twitter_api.update_status(tweet)


def main():
    twitter_api = config.create_api()
    monty_python_api = wrapper.MontyPythonAPI("v1")
    schedule.every(30).minutes.do(tweet_monty_python, twitter_api, monty_python_api)  # TESTING
    schedule.every(30).minutes.do(follow_followers, twitter_api)
    schedule.every(5).seconds.do(lambda: print("This prints every 5 seconds"))
    while True:
        run_pending()


if __name__ == '__main__':
    main()
    
