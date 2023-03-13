from time import sleep
import discord
import os
from dotenv import load_dotenv
import random
import json
import requests
import datetime
from discord.ext import tasks
from discord.ext import commands


# Use python-dotenv pakcage to get variables stored in .env file of your project
intents = discord.Intents().all()
client = commands.Bot(command_prefix="$", intents=intents)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DIFFBOT_TOKEN = os.environ.get("DIFFBOT_TOKEN")


hello_message = '''@everyone Hello, Read some engineering blogs right now.'''

with open("cache.json", "r") as f:
    cache = json.loads(f.read())

with open("seen.json", "r") as f:
    seen = json.loads(f.read())

with open("liked.json", "r") as f:
    liked = json.loads(f.read())

blogs = ["https://ai.googleblog.com/", 
         "https://blog.janestreet.com/", 
         "https://www.youtube.com/@StanfordMLSysSeminars/streams", 
         "https://www.uber.com/blog/virginia/engineering/ai/",
         "https://runwayml.com/blog/category/engineering/",
         "https://medium.com/airbnb-engineering/ai/home",
         "https://blog.comma.ai/",
         "https://medium.com/cruise/engineering/home",
         "https://www.youtube.com/@entreprenuership_opportunities/videos"
         ]

last_update = datetime.datetime.strptime(cache["time"], "%Y-%m-%d %H:%M:%S")

def update() -> None:
    current_time = datetime.datetime.now()
    if current_time - last_update > 3:
        for blog in cache:
            request_url = "https://api.diffbot.com/v3/list?token=" + DIFFBOT_TOKEN +  "&url=" + blog
            headers = {"accept": "application/json"}
            response = requests.get(request_url, headers=headers).json()
            print(response["objects"][0])
            cache[blog] = response["objects"][0]["items"]
            with open("cache.json", "w") as f:
                json.dump(cache, f)


def random_article() ->  str:
    blog = random.choice(blogs)
    text = ""
    if blog in cache:
        article = random.choice(cache[blog])
        if article["title"] in seen:
            article = random.choice(cache[blog])
        text += article["title"]+ "\n" + article["link"]
        seen.append(article["title"])
        cache["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("cache.json", "w") as f:
            json.dump(cache,f)
        with open("seen.json", "w") as f:
            json.dump(seen,f)

    else:
        request_url = "https://api.diffbot.com/v3/list?token=" + DIFFBOT_TOKEN +  "&url=" + blog
        headers = {"accept": "application/json"}
        response = requests.get(request_url, headers=headers).json()
        print(response["objects"][0])
        cache[blog] = response["objects"][0]["items"]
        article = random.choice(cache[blog])
        text += article["title"]+ "\n" + article["link"]
        with open("cache.json", "w") as f:
            json.dump(cache, f)

    return text

@client.event
async def on_ready():
  print(f'{client.user} is now online!')


@client.event
async def on_message(message): 
    if message.author == client.user:
        return  
    # lower case message
    message_content = message.content.lower()  


    if message.content.startswith(f'$hello'):
        await message.channel.send(hello_message)

    if message.content.startswith(f'$random'):
        await message.channel.send(random_article())

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user and str(reaction.emoji) in ['👍', '👎'] and reaction.message.author.id == client.user.id:
        message = reaction.message.content
        title = message.split("\n")[0]
        liked.append(title)
        with open("liked.json", "w") as f:
            json.dump(liked,f)
        print(f'{user} reacted with {reaction.emoji} to message {reaction.message.content}')



client.run(DISCORD_TOKEN) 