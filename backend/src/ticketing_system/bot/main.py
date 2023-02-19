import discord
import requests
import os
from discord import app_commands
from discord.ext import commands
from .issue_project.cog import IssueProject
from dotenv import load_dotenv


load_dotenv()

CHANNEL = "b"
CMD_CHANNEL = "b"
COMMAND_PREFIX = "!"
TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("CLIENT_SECRET")
MY_GUILD = discord.Object(id=636623317180088321)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.add_cog(IssueProject(bot))


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
