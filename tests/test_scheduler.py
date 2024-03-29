import time
import random

import schedule
from schedule import every, run_pending

from api_wrapper import wrapper
from app import handpicked_quotes, utils

api = wrapper.MontyPythonAPI()


def get_handpicked_quote():
    return random.choice(handpicked_quotes.quotes)
def get_random_quote():
    return utils.tweet_random_quote(api)
def get_random_sketch():
    return utils.tweet_random_sketch(api)


@schedule.repeat(every(1).second)
def print_every_second():
    print("Printed")


# @schedule.repeat(every(5).seconds)
# def print_quote():
#     print("QUOTE: " + utils.tweet_random_quote(api))


# @schedule.repeat(every(10).seconds)
# def print_sketch():
#     print("SKETCH: " + utils.tweet_random_sketch(api))


@schedule.repeat(every(5).seconds)
def print_random_choice_quotes():
    function_choices = [
        get_handpicked_quote,
        get_random_quote,
        get_random_sketch
    ]
    do_func = random.choice(function_choices)
    print(repr(do_func) + ": " + do_func())


if __name__ == "__main__":
    while True:
        run_pending()