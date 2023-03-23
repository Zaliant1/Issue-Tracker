import discord
import time
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
COOLDOWN_AMOUNT = 10.0  # seconds


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


last_executed = time.time()


def assert_cooldown():
    global last_executed
    if last_executed + COOLDOWN_AMOUNT < time.time():
        last_executed = time.time()
        return True
    return False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.load_extension("src.ticketing_system.bot.issue_project.cog")


@bot.event
async def on_message(message):
    tram_list = ["tram", "trams"]

    if not assert_cooldown():
        return

    if any(word in message.content.lower() for word in tram_list):
        print("saw tram")

        if message.author.bot:
            return
        with open("src/ticketing_system/bot/tram_copypasta.md") as target:
            tram_reply = target.read()

            await message.channel.send(
                tram_reply, reference=message, mention_author=False
            )

    if "risto" in message.content:
        print("saw risto")
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/825530277694144542/1077734017790656583/image.png",
            reference=message,
            mention_author=False,
        )


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
