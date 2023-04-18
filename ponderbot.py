import json
from fuzzywuzzy import fuzz
import os
import discord
from dotenv import load_dotenv
import re

# bot.py
load_dotenv()

# Load the JSON file
with open('unique-cards.json') as f:
    data = json.load(f)

def search(input_str):
    # Find the closest match to the input string
    max_score = 0
    closest_match = None
    for item in data:
        name = item['name']
        score = fuzz.ratio(name.lower(), input_str.lower())
        if score > max_score:
            max_score = score
            closest_match = item

    # Print the closest match
    if closest_match:
        if max_score > int(os.getenv('CONFIDENCE_THRESHOLD')):
            return ("Search: " + input_str + " (" + closest_match['name'] + ")", closest_match['image_uris']['large'], "Confidence: " + str(max_score) + "%")
        else:
            return ("Search: " + input_str, None, "Uncertain")

    else:
        print("No match found. ")


TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(command_prefix='$', intents=discord.Intents.all())
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message.content)
    if message.author.bot == False:
        searchls = re.findall('{.*?}', message.content)
        if (searchls != []):
            url_list = []
            name_list = []
            score_list = []

            for searchterm in searchls:
                output = search(searchterm.replace("}","").replace("{",""))
                
                name_list.append(output[0])
                if output[1]: url_list.append(output[1])
                score_list.append(output[2])

            outstr = ""
            if len(url_list) > 0: outstr = "\n".join(url_list) + "\n"
            for x in range(len(name_list)):
                outstr += name_list[x] + " (" + score_list[x] + "). \n"
            
            await message.channel.send(outstr, reference=message)
            

client.run(TOKEN)