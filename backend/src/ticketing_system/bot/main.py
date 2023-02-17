import discord
from discord import ui, app_commands
from discord.ext import commands
import requests

# from discord.ui import Select, View, Button, TextInput, Modal
import os
import json
from dotenv import load_dotenv
from ..api import webhooks

load_dotenv()

CHANNEL = "b"
CMD_CHANNEL = "b"
COMMAND_PREFIX = "?"
TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("CLIENT_SECRET")

MY_GUILD = discord.Object(id=636623317180088321)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=MY_GUILD)

    async def on_guild_join(self, guild):
        await self.tree.sync(guild=guild)


client = Bot(intents=intents)


class MyModal(discord.ui.Modal):
    category = ui.TextInput(
        label="category",
        placeholder="Issue Category",
    )

    player = ui.TextInput(
        label="player",
        placeholder="Player Name",
    )

    version = ui.TextInput(
        label="version",
        placeholder="Version",
    )

    issue_type = ui.TextInput(
        label="issue",
        placeholder="bug or suggestion",
    )

    summary = ui.TextInput(
        label="summary",
        placeholder="Issue Summary",
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        issue = {
            "status": "reported",
            "summary": self.summary.value,
            "category": self.category.value,
            "type": self.issue_type.value,
            "priority": "high",
            "playerName": self.player.value,
            "version": self.version.value,
            "description": "",
            "modLogs": {
                "title": "",
                "body": "",
            },
            "archived": False,
            "attachments": {"embedSource": "", "generalUrl": ""},
        }

        response = requests.put(
            "http://localhost:8000/api/issue",
            json=issue,
        ).json()

        await interaction.response.send_message(
            f"http://localhost:3000/issue/{response}"
        )


@client.tree.command(name="modaltest")
async def modaltest(interaction: discord.Interaction):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="New Issue Submission")
    await interaction.response.send_modal(modal)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()