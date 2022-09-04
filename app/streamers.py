import tweepy

import logging

logger = logging.getLogger()


class HashTagsChecker(tweepy.StreamingClient):
    """Filters for specific hashtags and interacts with them"""

    def __init__(self, bearer_token, client):
        super().__init__(bearer_token)
        self.client = client
    
    def on_tweet(self, tweet):
        logger.info(
            f"{tweet.id} {tweet.created_at} ({tweet.author_id}): {tweet.text}")
        
        if tweet.text.startswith("RT"):  # Don't interact with retweets.
            return
        
        # Like the tweet.
        try:
            response_like = self.client.like(tweet.id)
            logger.info(f"Liked!: {response_like}")
        except tweepy.TweepyException as e:
            logger.error(f"Error on favoriting: {e}")

        # Retweet the tweet.
        try:
            response_retweet = self.client.retweet(tweet.id)
            logger.info(f"Retweeted!: {response_retweet}")
        except tweepy.TweepyException as e:
            logger.error(f"Error on retweeting: {e}")
    
    def on_error(self, error):
        logger.error(f"Error: {error}")

