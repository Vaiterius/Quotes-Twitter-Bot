"""A Twitter bot that tweets daily Monty Python quotes"""
import time
import logging
import random

import tweepy
import schedule
from schedule import run_pending

from app import handpicked_quotes, utils, config, responses
from api_wrapper import wrapper

# Create and configure logger.
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
logger = logging.getLogger()


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
        logger.info("Tweeting a handpicked quote")
        tweet += random.choice(handpicked_quotes.quotes)
    elif choice_function == 1:
        logger.info("Tweeting a random API quote")
        tweet += utils.tweet_random_quote(monty_python_api)
    else:
        logger.info("Tweeting random API sketch dialogue")
        tweet += utils.tweet_random_sketch(monty_python_api)
    
    # API probably not working?
    if not tweet:
        logger.error("Error occurred")
        raise Exception("Error occurred")
    
    twitter_api.update_status(tweet)
    logger.info(f"Tweeted: {tweet}")


def main():
    logger.info("Initializing app")
    twitter_api = config.create_api()
    monty_python_api = wrapper.MontyPythonAPI()
    schedule.every(30).minutes.do(tweet_monty_python, twitter_api, monty_python_api)
    schedule.every(1).minute.do(follow_followers, twitter_api)
    while True:
        run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
    
