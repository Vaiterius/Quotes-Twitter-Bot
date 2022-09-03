import random

from app import movie_quotes

MAX_LENGTH = 280


def get_tweetable_sketch(sketch):
    """Return a random subsection of lines of dialogue that fit within 280 chars"""
    sketch_lines: list = sketch["body"]
    
    # Load dialogue lines.
    dialogue = "\n".join(sketch_lines)
    
    # Already of tweetable length.
    if len(dialogue) <= MAX_LENGTH:
        return dialogue
    
    truncated_dialogue = ""
    EPSILON = 100
    random_index = random.randrange(0, len(sketch_lines))
    while len(truncated_dialogue) < MAX_LENGTH:
        
        if (MAX_LENGTH - len(truncated_dialogue)) <= EPSILON:
            break
        if random_index > len(sketch_lines) - 1:
            return ""
        
        next_lines = truncated_dialogue + "\n" + sketch_lines[random_index]
        if len(next_lines) > MAX_LENGTH:
            return ""
        
        truncated_dialogue += "\n" + sketch_lines[random_index]
        random_index += 1
        
    return truncated_dialogue.strip()


def tweet_random_sketch(api) -> None|str:
    sketch = api.get_random_sketch(detailed=False)
    
    if not isinstance(sketch, dict):
        print("No sketch found...")
        return None
    
    # Loop until tweetable dialogue is found.
    tweetable_dialogue = get_tweetable_sketch(sketch)
    while tweetable_dialogue == "":
        sketch = api.get_random_sketch(detailed=False)
        tweetable_dialogue = get_tweetable_sketch(sketch)

    return tweetable_dialogue


def tweet_random_quote(api) -> None|str:
    quote = api.get_random_quote(min_length=15, max_length=MAX_LENGTH)
    
    if not isinstance(quote, dict):
        print("No quote found...")
        return None
    
    tweetable_quote = quote["quote"]
    while len(tweetable_quote) > 280:
        print("Invalid length for quote")
        tweetable_quote = api.get_random_quote(
            min_length=15, max_length=MAX_LENGTH)["quote"]
    
    return tweetable_quote

