"""A Twitter bot that tweets daily Monty Python quotes"""
import os
import time
import logging
import random
import platform

import tweepy
import schedule
from schedule import run_pending
from dotenv import load_dotenv

from app import handpicked_quotes, utils
from api_wrapper import wrapper

load_dotenv()

# Create and configure logger.
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
logger = logging.getLogger()


def main():
    # On startup.
    logger.info("Connected!")
    logger.info(f"Using Tweepy v{tweepy.__version__}")
    logger.info(f"Using Python v{platform.python_version()}")
    logger.info(
        f"Runing on {platform.system()} {platform.release()} ({os.name})")
    logger.info("And now for a completely different bot...")
    logger.info("-----------------------------------------")
    
    twitter_api = get_client()
    monty_python_api = wrapper.MontyPythonAPI()
    
    # Tweet something on bot startup.
    tweet_monty_python(twitter_api, monty_python_api)

    # Tweet every 3 hours.
    schedule.every(3).hours.do(
        tweet_monty_python, twitter_api, monty_python_api)
    
    while True:
        run_pending()
        time.sleep(1)


def get_client() -> tweepy.Client:
    """Authenticate and initialize V2 bot client"""
    return tweepy.Client(
        bearer_token=os.environ.get("BEARER_TOKEN"),
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_KEY_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
        wait_on_rate_limit=True)


class Tweeter:
    """Tweet string generator for Monty Python Quotes"""
    def __init__(self, api: wrapper.MontyPythonAPI):
        self._api = api

    def tweet_handpicked(self) -> str:
        logger.info("Tweeting a handpicked quote:")
        return random.choice(handpicked_quotes.quotes)


    def tweet_quote(self) -> str:
        logger.info("Tweeting a random API quote:")
        return utils.tweet_random_quote(self._api)


    def tweet_sketch(self) -> str:
        logger.info("Tweeting random API sketch dialogue:")
        return utils.tweet_random_sketch(self._api)


def tweet_monty_python(
        twitter_client: tweepy.Client,
        monty_python_api: wrapper.MontyPythonAPI):
    """
    Tweets either:
    - A handpicked quote from a list
    - A random quote from the API
    - Random sketch dialogue from the API
    """
    tweeter = Tweeter(monty_python_api)
    tweet_func: callable = random.choice([
        tweeter.tweet_handpicked, tweeter.tweet_quote, tweeter.tweet_sketch
    ])

    tweet: str = tweet_func()
    
    # API probably not working?
    if not tweet:
        logger.error("API Error")
        return
    
    try:
        twitter_client.create_tweet(text=tweet)
        logger.info(f"{tweet}")
    except tweepy.TweepyException as e:
        logger.error(e)
    
    return


if __name__ == '__main__':
    main()
