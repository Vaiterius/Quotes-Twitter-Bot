"""
Gooby Bot: Experimental Twitter bot by Vaiterius.
"""

import os
import time
import json
import random
import logging

import tweepy
from better_profanity import profanity

# Create and configure logger.
LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(filename="log.txt",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode = "w")
logger = logging.getLogger()

# Import subjects for bot to interact with.
with open("victims.json") as users_file:
    users_dict = json.load(users_file)
# Import Monty Python quotes.
with open("monty_python_quotes.json", encoding="utf-8") as file:
    quotes_list = json.load(file)


class CustomListener(tweepy.StreamListener):
    """Actively listen to new user tweets, personally selected."""
    
    def __init__(self, api, victim_dict, hashtags_list):
        self.api = api
        self.me = api.me()
        self.victim_dict = victim_dict
        self.victim_names = [value["screen_name"] for id, value in victim_dict.items()]
        self.victim_ids = [id for id in victim_dict]
        self.hashtags_list = hashtags_list
        print(f"Selected users: \nNames: {self.victim_names}\nID's: {self.victim_ids}")
        logger.info(f"Selected users: \nNames: {self.victim_names}\nID's: {self.victim_ids}")
    
    def on_status(self, status):
        """Simple algorithm to check if victim has allowed likes, retweets, and/or replies."""
        tweet = status.text
        tweet_id = status.id
        user = status.user.screen_name
        print("CHECK CHECK CHECK", tweet)
        print("This person just tweeted:", user)
        logger.info("This person just tweeted:", user)
        
        for id, id_info in self.victim_dict.items():
            current_iter = id_info["screen_name"]
            print("Current iter:", current_iter)
            if current_iter.lower() == user.lower():
                print("That's the one!")
                logger.info("That's the one!")
                for action, bool in id_info.items():
                    # Calls another method to reply to tweet if enabled.
                    if action == "enable_reply" and bool is True:
                        print("Replied to tweet!")
                        logger.info("Replied to tweet!")
                        self.make_reply(tweet, tweet_id, user)

                    try:
                        # Like victim's tweet if enabled.
                        if action == "enable_like" and bool is True:
                            print("Liked tweet!")
                            logger.info("Liked tweet!")
                            self.api.create_favorite(tweet_id)
                    except tweepy.TweepError as e:
                        print(e.response.text)
                        logger.info(e.response.text)

                    try:
                        # Retweet victim's tweet if enabled.
                        if action == "enable_retweet" and bool is True:
                            print("Retweeted tweet!")
                            logger.info("Retweeted tweet!")
                            self.api.retweet(tweet_id)
                    except tweepy.TweepError as e:
                        print(e.response.text)
                        logger.info(e.response.text)
            else:
                print("Not looking for this one.")
                logger.info("Not looking for this one.")
        
        logger.error("End of iteration.")
        print("End of iteration.")

    def make_reply(self, tweet, tweet_id, user):
        """Reply to user tweet with some funny/roast stuff."""
        # Import funny/roast responses as dictionary.
        with open("listener_responses.json") as dict_file:
            responses_dict = json.load(dict_file)

        # Avoid tweets not made by the victims (retweets).
        if user.lower() not in self.victim_names or "RT @" in tweet:
            pass
        else:
            rand_float = random.random()
            print(f"FOUND: {tweet}")
            logger.info(f"FOUND: {tweet}")

            if rand_float > 0.25:  # Bot gives funny reply in user tweet.
                bot_pick = random.choice(responses_dict["funny_responses"])
                bot_reply = f"@{user} {bot_pick}"
                self.api.update_status(bot_reply, tweet_id)
            else:  # Bot roasts user in their tweet.
                bot_pick = random.choice(responses_dict["roast_responses"])
                bot_reply = f"@{user} {bot_pick}"
                self.api.update_status(bot_reply, tweet_id)

    def on_data(self, data):
        """Receive raw data from stream and handle sending data to other methods."""
        # Parses data from string to readable dict format.
        parsed_data = json.loads(data)

        # This chunk was copied and pasted from original source code since this whole method overwrote it.
        # Essential in case data received is different than expected, having many forms.
        if "delete" in parsed_data:
            delete = parsed_data["delete"]["status"]
            return self.on_delete(delete["id"], delete["user_id"])
        if "disconnect" in parsed_data:
            return self.on_disconnect_message(parsed_data["disconnect"])
        if "limit" in parsed_data:
            return self.on_limit(parsed_data["limit"]["track"])
        if "scrub_geo" in parsed_data:
            return self.on_scrub_geo(parsed_data["scrub_geo"])
        if "status_withheld" in parsed_data:
            return self.on_status_withheld(parsed_data["status_withheld"])
        if "user_withheld" in parsed_data:
            return self.on_user_withheld(parsed_data["user_withheld"])
        if "warning" in parsed_data:
            return self.on_warning(parsed_data["warning"])

        # Find if data contains hashtag from hashtags list.
        print("DATA RECEIVED:", parsed_data)
        logger.info("DATA RECEIVED")
        for hashtag in self.hashtags_list:
            # If hashtag is found inside text and author is not self.
            if hashtag in parsed_data["text"] and self.me.id != parsed_data["user"]["id"]:
                print(f"{hashtag} FOUND")
                logger.info(f"{hashtag} FOUND")
                user_name = parsed_data["user"]["screen_name"]
                reply = f"@{user_name} I'm Goobybot!"
                try:
                    self.api.create_favorite(parsed_data["id"])
                    self.api.retweet(parsed_data["id"])
                except tweepy.TweepError as e:
                    print(e.response.text)
                    logger.info(e.response.text)
                finally:
                    self.api.update_status(reply, parsed_data["id"])
                    print(f"I replied with: {reply}")
                    logger.info(f"I replied with: {reply}")
        
        # Continue to on_status() method when finished processing data.
        if "in_reply_to_status_id" in parsed_data:
            status = tweepy.models.Status.parse(None, parsed_data)
            return self.on_status(status)
    
        logger.error("Received unknown message type data.")

    def on_error(self, status_code):
        """Returning False disconnects the stream if something went wrong."""
        if status_code == 420:
            print("Error detected while listening.")
            logger.info("Error detected while listening.")
            return False


def create_api() -> object:
    """Build API object after retrieving credentials."""

    API_KEY = os.environ["API_KEY"]
    API_KEY_SECRET = os.environ["API_KEY_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

    # Authenticate to Twitter.
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object.
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Test credentials.
    try:
        api.verify_credentials()
        print("API object created.")
        logger.info("API object created.")
    except:
        print("Error creating API obect.")
        logger.error("Error creating API obect.")
        raise Exception("Error creating API obect.")
    
    return api


def follow_followers(api):
    """Follow anyone that follows bot."""
    
    print("Retrieving and following followers.")
    logger.info("Retrieving and following followers.")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            print(f"Following {follower.name}")
            logger.info(f"Following {follower.name}")
            follower.follow()


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


def check_mentions(api, FILE_NAME):
    """Check to see if anyone @'s the bot and reply accordingly."""
    # Import offensive key phrases with responses to them.
    with open("profanity_responses.json") as file:
        p_responses_list = json.load(file)

    print("Checking mentions.")
    logger.info("Checking mentions.")
    mentions = api.mentions_timeline(read_last_seen_id(FILE_NAME), tweet_mode="extended")
    
    # Sus replies, delete soon lol.
    replies = [
        "What's good fam?", "You tryna kiss me or sum?", "Damn homie I think you lookin' cute",
        "Hey boo", "Balls in my face", "Shut up before I kiss you", "Hey daddy", "Can I be your baby daddy?",
        "Hey lol", "You kinda cute doe", "Daddy chill", "You be fartin' a lot?", "Ey lemme smack that ass tho",
        "Hola papi", "You be squirtin'?", "Lemme smell that fart tho", "DM me feet pics", "sex",
        "Butt ass naked replying to you rn", "Do it jiggle?", "Dick me down I go dicko mode", "lol"
        ]
    
    for mention in reversed(mentions):
        # Bot does not mention itself, which leads to an infinite loop.
        if mention.user.screen_name != api.me().screen_name:
            print(f"[MENTION] {mention.id} - {mention.full_text}")

            # Check for any offensive mentions and reply to it.
            if profanity.contains_profanity(mention.full_text):
                print("Responding to offensive tweet.")
                logger.info("Responding to offensive tweet.")
                response = random.choice(p_responses_list)
                api.update_status(f"@{mention.user.screen_name} {response}", mention.id)
                store_last_seen_id(FILE_NAME, mention.id)
                return

            # If not, respond normally to mention and also like and retweet.
            try:
                print("Responding to normal tweet...")
                logger.info("Responding to normal tweet...")
                api.create_favorite(mention.id)
                api.retweet(mention.id)
            except tweepy.TweepError as e:
                print(e.response.text)
                logger.info(e.response.text)
            finally:
                api.update_status(f"@{mention.user.screen_name} {random.choice(replies)}", mention.id)
                store_last_seen_id(FILE_NAME, mention.id)
            return

### SAVE FOR LATER ###
# def handle_messages(api):
#     messages_list = api.list_direct_messages()
#     print("MESSAGE LIST:", messages_list)
#     logger.info("MESSAGE LIST:", messages_list)
#     last_id = 1  # We only wanted the last ones.
#     test_counter = 1
#     bot_reply = f"{test_counter} Hi, Gouby here! This is just a sample message."
    
#     # Go through every sent/received message in bot's DMs.
#     for message in messages_list:
#         current_id = message.id
#         print(f"Fetching ID: {current_id}")
#         logger.inof(f"Fetching ID: {current_id}")
#         message_object = api.get_direct_message(current_id, full_text=True)


def tweet_quote(api):
    """Tweets a Monty Python quote every 2 hours."""
    # Randomly picks quote from list, tweets it, then add to already quoted.
    already_quoted = []
    while len(already_quoted) != len(quotes_list):
        selected_quote = random.choice(quotes_list)
        if selected_quote in already_quoted:
            # Pass if quote has already been chosen in current cycle.
            continue
        else:
            print(f'Tweeting quote... "{selected_quote}"')
            logger.info(f'Tweeting quote... "{selected_quote}"')
            try:
                api.update_status(f'"{selected_quote}"')
            except tweepy.TweepError as e:
                print(e.response.text)
                logger.info(e.response.text)
            finally:
                already_quoted.append(selected_quote)
                return
    # If both lists are already same length (all quotes have been
    # used at least once), then clear. This restarts process.
    already_quoted.clear()


def main():
    hashtags_list = ["#goobybot", "#montypythonquotes"]
    # API initialization.
    api = create_api()
    # Receives tweets from the stream.
    stream_listener = CustomListener(api, users_dict, hashtags_list)
    # Uses API to get tweets that match some criteria -- source of tweets processed by stream listener.
    stream = tweepy.Stream(auth = api.auth, listener=stream_listener)

    # Connect and start stream object filtering.
    # is_async=True allows the listener to run on another thread so that the
    # main loop will run at the same time.
    stream.filter(follow=[id for id in users_dict], track=hashtags_list, is_async=True)

    # NUM_MIN: 60 for 1 hour, 120 for 2 hours...
    NUM_MIN = 360
    mod_counter = 180

    # Calls all bot functions every minute so as to not be rate limited.
    while True:
        # Tweets quote every x hours, depending on NUM_MIN.
        if mod_counter % NUM_MIN == 0:
            tweet_quote(api)
            mod_counter = 1

        mod_counter += 1
        print(f"Counter is now: {mod_counter}")
        logger.info(f"Counter is now: {mod_counter}")

        # handle_messages(api)
        follow_followers(api)
        check_mentions(api, "last_seen.txt")
        logger.info("Waiting...")
        print("Waiting...")
        time.sleep(70)


if __name__ == '__main__':
    main()
