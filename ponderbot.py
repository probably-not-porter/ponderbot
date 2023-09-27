#     _______                            __                      __                    __     
#    /       \                          /  |                    /  |                  /  |    
#    $$$$$$$  | ______   _______    ____$$ |  ______    ______  $$ |____    ______   _$$ |_   
#    $$ |__$$ |/      \ /       \  /    $$ | /      \  /      \ $$      \  /      \ / $$   |  
#    $$    $$//$$$$$$  |$$$$$$$  |/$$$$$$$ |/$$$$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$  |$$$$$$/   
#    $$$$$$$/ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ $$ |  $$ |$$ |  $$ |  $$ | __ 
#    $$ |     $$ \__$$ |$$ |  $$ |$$ \__$$ |$$$$$$$$/ $$ |      $$ |__$$ |$$ \__$$ |  $$ |/  |
#    $$ |     $$    $$/ $$ |  $$ |$$    $$ |$$       |$$ |      $$    $$/ $$    $$/   $$  $$/ 
#    $$/       $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/ $$/       $$$$$$$/   $$$$$$/     $$$$/  
#                                                                                         
#                                             v1.0   /   April 2023   /   Porter Libby                                                                              
#                                                                                         
################# Imports #################
import json
from fuzzywuzzy import fuzz
import os
import discord
from dotenv import load_dotenv
import re

################# BOT SETUP #################
# Set up bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(command_prefix='$', intents=discord.Intents.all())

# Load card data
with open(os.getenv('DATA_PATH')) as f:
    data = json.load(f)

################# FUZZY SEARCH #################
def search(input_str):
    # Find the closest match to the input string
    max_score = 0 # highest probability of a matching term
    closest_match = None
    for item in data:
        name = item['name']
        score = fuzz.ratio(name.lower(), input_str.lower()) # calculate probability

        # if probability good, set as new best choice
        if score > max_score:
            max_score = score
            closest_match = item

    # Print the closest match
    if closest_match:
        if max_score > int(os.getenv('CONFIDENCE_THRESHOLD')):
            # if match is good enough to return to use
            return ("Search: " + input_str + " (" + closest_match['name'] + ")", closest_match['image_uris']['large'], "Confidence: " + str(max_score) + "%")
        else:
            # if match is not good enough
            return ("Search: " + input_str, None, "Uncertain")

############# DISCORD MESSAGE EVENT #############
@client.event
async def on_message(message):
    if message.author.bot == False:
        # Search message for {terms}
        searchls = re.findall('{.*?}', message.content)

        # If there are {terms}
        if (searchls != []):
            url_list = []
            name_list = []
            score_list = []

            # for each term
            for searchterm in searchls:
                output = search(searchterm.replace("}","").replace("{","")) # search for matching cards
                name_list.append(output[0])
                if output[1]: url_list.append(output[1])
                score_list.append(output[2])

            # Create output string
            outstr = ""
            if len(url_list) > 0: outstr = "\n".join(url_list) + "\n"
            for x in range(len(name_list)): outstr += name_list[x] + " (" + score_list[x] + "). \n"

            # Send message reply to user
            await message.channel.send(outstr, reference=message)
            
################# START BOT #################
client.run(TOKEN)
