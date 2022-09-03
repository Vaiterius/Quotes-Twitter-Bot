from api_wrapper import wrapper
from app import utils

api = wrapper.MontyPythonAPI("v1")

MAX_LENGTH = 280


def test_tweetable_quotes():
    NUM_TESTS = 50
    with open("tests/test_quote_tweets.txt", "w") as file:
        for i in range(NUM_TESTS):
            quote = utils.tweet_random_quote(api)
            len_quote = len(quote)
            flag = ""
            if len_quote > MAX_LENGTH:
                print(f"Above max length! ({len_quote})")
                flag += "***** "
            file.write(flag + f"LENGTH: {len_quote}\n")
            file.write(quote + "\n\n")


if __name__ == "__main__":
    test_tweetable_quotes()

