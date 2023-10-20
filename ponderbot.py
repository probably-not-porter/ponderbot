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
#                                             v1.1   /   April 2023   /   Porter Libby                                                                              
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
    reverse_mode = False
    if input_str[0] == "!":
        input_str = input_str[1:]
        reverse_mode = True
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
            if reverse_mode == False:
                # if match is good enough to return to use
                return ("Search: " + input_str + " (" + closest_match['name'] + ")", closest_match['image_uris']['large'], "Confidence: " + str(max_score) + "%")
            else:
                return reverse_search(closest_match)
        else:
            # if match is not good enough
            return ("Search: " + input_str, None, "Uncertain")
        
################# FUZZY REVERSE SEARCH #################
def reverse_search(card):
    best_scores = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    best_items = [None,None,None,None,None,None,None,None,None,None]
    names = []
    for item in data:
        if item['name'] != card['name']:
            otext_score = 0
            type_score = 0
            cost_score = 0
            if "oracle_text" in item:
                otext_score = fuzz.ratio(card['oracle_text'], item['oracle_text'])
            if 'type_line' in item:
                type_score = fuzz.ratio(card['type_line'], item['type_line'])
            if 'mana_cost' in item:
                cost_score = fuzz.ratio(card['mana_cost'], item['mana_cost'])

            total_score = (otext_score * 0.8) + (type_score * 0.1) + (cost_score * 0.1)
            for b in range(len(best_scores)):
                bscore = best_scores[b]
                if total_score > bscore and item['name'] not in names:
                    names.append(item['name'])
                    best_scores[b] = total_score
                    best_items[b] = item
                    break
    out_text = "\n"
    for i in range(len(best_scores)):
        out_text += best_items[i]['name'] + " (" + str(round(best_scores[i],2)) + "%)\n" + best_items[i]['image_uris']['large'] + "\n"
    #return ("Search: input term (reverse)", "image", "list with closeness?")
    return ("Search: " + card['name'] + "\n", card['image_uris']['large'], out_text)

############# SEND EMBED ##############
async def sendEmbed():
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await message.channel.send(embed=embedVar)


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
