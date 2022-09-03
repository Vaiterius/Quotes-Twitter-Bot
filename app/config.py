import os
import logging

import tweepy
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()


def create_api() -> object:
    """Build API object after retrieving credentials."""

    API_KEY = os.environ.get("API_KEY")
    API_KEY_SECRET = os.environ.get("API_KEY_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

    # Authenticate to Twitter.
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object.
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Test credentials.
    try:
        api.verify_credentials()
        logger.info("API object created.")
    except:
        logger.error("Error creating API obect.")
        raise Exception("Error creating API obect.")
    
    return api

