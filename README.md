# Monty Python Quotes Twitter Bot

A fun bot that tweets random quotes from Monty Python on the daily.

Utilizes Python wrapper *[tweepy](https://github.com/tweepy/tweepy)*, tweet scheduling with *[schedule](https://schedule.readthedocs.io/en/stable/)*, and deployed with *[Docker](https://www.docker.com/)*. Hosted on *[Fly.io](https://fly.io/)*.

All quotes are sourced from a quotes API I wrote *[here](https://github.com/Vaiterius/Monty-Pythons-Flying-API)* as well as some hand-picked ones.

## What it does
- Tweet a Monty Python quote every once in a while
- Filters tweets in real-time to pick out chosen hashtags and likes/retweets them
- Follow anyone that follows bot

Twitter handle: *[@bot_gooby](https://twitter.com/bot_gooby)*