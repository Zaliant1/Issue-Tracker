import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

CHANNEL = "b"
CMD_CHANNEL = "b"
COMMAND_PREFIX = "!"
TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("CLIENT_SECRET")



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)




def get_data(category):
    response = requests.get(f"http://127.0.0.1:8000/api/category/{category}")
    json_response = json.loads(response.json())

    return json.dumps({
        "status": json_response[0]['status'],
        "category": json_response[0]['category'],
        "priority": json_response[0]['priority'],
        "version": json_response[0]['version'],
        "player": json_response[0]['playerName']
    }, indent=2)
    


async def get_new(ctx, data):
    await ctx.send(data)



@bot.command()
async def category(ctx, input):
    await ctx.send(get_data(input))


@bot.command(name="hi")
async def cmd(ctx):
    print(list(bot.get_all_channels()))
    await ctx.send("sdfsd")



def main():
    bot.run(TOKEN)
    
    return "i'm running"


if __name__ == "__main__":
    main()