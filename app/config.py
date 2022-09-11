import os
import logging

import tweepy
from dotenv import load_dotenv

from app import streamers

load_dotenv()
logger = logging.getLogger()

API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")


def create_api() -> "tweepy.API":
    """Build API object after retrieving credentials."""

    # Authenticate to Twitter.
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object.
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Test credentials.
    try:
        api.verify_credentials()
        logger.info("API object created")
    except:
        logger.error("Error creating API obect")
        raise Exception("Error creating API obect")
    
    return api


def get_client() -> "tweepy.Client":
    """Build API client for action functionalities"""
    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True)


def get_stream_listener() -> "tweepy.StreamingClient":
    """Build streaming object to filter real-time tweets"""
    return streamers.HashTagsChecker(
        BEARER_TOKEN, wait_on_rate_limit=True, client=get_client())

