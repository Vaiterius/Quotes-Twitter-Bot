"""A Twitter bot that tweets daily Monty Python quotes"""
import time
import logging
import random

import tweepy
import schedule
from schedule import run_pending

from app import handpicked_quotes, utils, config
from api_wrapper import wrapper

# Create and configure logger.
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
logger = logging.getLogger()


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
    tweet = ""
    choice_function = random.randint(0, 2)
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
        logger.error("API Error")
        return
    
    try:
        twitter_api.update_status(tweet)
        logger.info(f"Tweeted: {tweet}")
    except tweepy.TweepyException as e:
        logger.error(e)
    
    return


def main():
    logger.info("Initializing app")
    twitter_api = config.create_api()
    monty_python_api = wrapper.MontyPythonAPI()
    
    # V2 tweets streaming.
    hashtags_checker = config.get_stream_listener()
    hashtags = ["#GoobyBot", "#MontyPythonQuotes"]
    for hashtag in hashtags:
        hashtags_checker.add_rules(tweepy.StreamRule(value=hashtag))
    hashtags_checker.filter(  # Explicitly include more payload details.
        expansions="author_id",
        tweet_fields="created_at",
        threaded=True)
    
    # Perform bot actions at scheduled times.
    schedule.every(3).hours.do(
        tweet_monty_python, twitter_api, monty_python_api)
    schedule.every(1).minute.do(follow_followers, twitter_api)
    
    while True:
        run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
