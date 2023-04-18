# Ponderbot
Ponder the orb at full speed. 
For if you don't want all that extra stuff from an mtg bot, just wanna see the picture of the card when you type {lightning bolt}.

Supports pretty wide misspellings.

## Setup
1. Create a discord bot token, and make a `.env` file:
```
# .env
DISCORD_TOKEN=[TOKEN]
CONFIDENCE_THRESHOLD=[1-100]
```
2. run `./get_cards.sh` to download the data.
3. `pip3 install python-dotenv fuzzywuzzy discord.py` to download dependencies.
4. `python3 ponderbot.py` to start.