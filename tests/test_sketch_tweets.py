from api_wrapper import wrapper
from app import utils

api = wrapper.MontyPythonAPI("v1")

MAX_LENGTH = 280


def test_tweetable_sketches():
    NUM_TESTS = 50
    with open("tests/test_sketch_tweets.txt", "w") as file:
        for i in range(NUM_TESTS):
            dialogue = utils.tweet_random_sketch(api)
            len_dialogue = len(dialogue)
            flag = ""
            if len_dialogue > MAX_LENGTH:
                print(f"Above max length! ({len_dialogue})")
                flag += "***** "
            file.write(flag + f"LENGTH: {len_dialogue}\n")
            file.write(dialogue + "\n\n")


if __name__ == "__main__":
    test_tweetable_sketches()

