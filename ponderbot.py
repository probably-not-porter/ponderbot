import json
from fuzzywuzzy import fuzz
import os
import discord
from dotenv import load_dotenv
import re

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
        return (closest_match['name'], closest_match['image_uris']['large'], max_score)
    else:
        print("No match found. ")

# bot.py
load_dotenv()
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
                url_list.append(output[1])
                score_list.append(output[2])

            outstr = "\n".join(url_list) + "\n"
            for x in range(len(url_list)):
                outstr += "Found '" + name_list[x] + "' (confidence: " + str(score_list[x]) + "). "
            
            await message.channel.send(outstr, reference=message)
            

client.run(TOKEN)