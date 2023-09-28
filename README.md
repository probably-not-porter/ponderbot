```
     _______                            __                      __                    __     
    /       \                          /  |                    /  |                  /  |    
    $$$$$$$  | ______   _______    ____$$ |  ______    ______  $$ |____    ______   _$$ |_   
    $$ |__$$ |/      \ /       \  /    $$ | /      \  /      \ $$      \  /      \ / $$   |  
    $$    $$//$$$$$$  |$$$$$$$  |/$$$$$$$ |/$$$$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$  |$$$$$$/   
    $$$$$$$/ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ $$ |  $$ |$$ |  $$ |  $$ | __ 
    $$ |     $$ \__$$ |$$ |  $$ |$$ \__$$ |$$$$$$$$/ $$ |      $$ |__$$ |$$ \__$$ |  $$ |/  |
    $$ |     $$    $$/ $$ |  $$ |$$    $$ |$$       |$$ |      $$    $$/ $$    $$/   $$  $$/ 
    $$/       $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/ $$/       $$$$$$$/   $$$$$$/     $$$$/  
                                                                                         
                                             v1.1   /   April 2023   /   Porter Libby 
```
Ponder the orb at full speed. 
For if you don't want all that extra stuff from an mtg bot, just wanna see the picture of the card when you type {lightning bolt}.

Supports pretty wide misspellings.

## Setup
1. Create a discord bot in the discord dev portal.
2. Add the bot to your server.
3. Create a `.env` file:
```
# .env
DISCORD_TOKEN=[TOKEN]
CONFIDENCE_THRESHOLD=[1-100]
DATA_PATH=/path/to/card/data
```
4. run `./get_cards.sh` to download the data.
5. `pip3 install python-dotenv fuzzywuzzy discord.py` to download dependencies.
6. `python3 ponderbot.py` to start.
