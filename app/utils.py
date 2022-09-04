import random

MAX_TWEET_LENGTH = 280


def get_tweetable_sketch(sketch):
    """Return a random subsection of lines of dialogue that fit within 280 chars"""
    sketch_lines: list = sketch["body"]
    
    # Load dialogue lines.
    dialogue = "\n".join(sketch_lines)
    
    # Already of tweetable length.
    if len(dialogue) <= MAX_TWEET_LENGTH:
        return dialogue
    
    truncated_dialogue = ""
    EPSILON = 100  # 
    random_index = random.randrange(0, len(sketch_lines))  # Random line from list.
    
    # Finding dialogue within max length.
    while len(truncated_dialogue) < MAX_TWEET_LENGTH:
        
        # Tweet length is good enough i.e. within epsilon value.
        if (MAX_TWEET_LENGTH - len(truncated_dialogue)) <= EPSILON:
            break
        # Prevent index error.
        if random_index > len(sketch_lines) - 1:
            return ""
        
        # Check to see if the next line can fit.
        next_lines = truncated_dialogue + "\n" + sketch_lines[random_index]
        if len(next_lines) > MAX_TWEET_LENGTH:
            return ""
        
        truncated_dialogue += "\n" + sketch_lines[random_index]
        random_index += 1
        
    return truncated_dialogue.strip()


def tweet_random_sketch(api) -> None|str:
    """Return dialogue from a random sketch truncated to fit a tweet"""
    sketch = api.get_random_sketch(detailed=False)
    
    if not isinstance(sketch, dict):  # Server probably not working.
        print("No sketch found...")
        return None
    
    # Loop until tweetable dialogue is found.
    tweetable_dialogue = get_tweetable_sketch(sketch)
    while tweetable_dialogue == "":
        sketch = api.get_random_sketch(detailed=False)
        tweetable_dialogue = get_tweetable_sketch(sketch)

    return tweetable_dialogue


def tweet_random_quote(api) -> None|str:
    """Return a random quote that fits a tweet"""
    quote = api.get_random_quote(min_length=15, max_length=MAX_TWEET_LENGTH)
    
    if not isinstance(quote, dict):  # Server probably not working.
        print("No quote found...")
        return None
    
    tweetable_quote = quote["quote"]
    while len(tweetable_quote) > 280:
        print("Invalid length for quote")
        tweetable_quote = api.get_random_quote(
            min_length=15, max_length=MAX_TWEET_LENGTH)["quote"]
    
    return tweetable_quote

