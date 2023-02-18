import discord
import requests
import os
from discord import ui, app_commands, Color
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


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_guild_join(self, guild):
        await self.tree.sync(guild=guild)


client = Client(intents=intents)


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
        embed = discord.Embed(
            title="Issue Created!",
            description=f"You can go [here](http://localhost:3000/issue/{response}) to fill out modlogs, attachments, and description",
            color=Color.blurple(),
        )

        await interaction.response.send_message(embed=embed)


@client.tree.command(name="add-issue")
async def add_issue_modal(interaction: discord.Interaction):
    """Brings up a modal to submit a new issue"""
    modal = MyModal(title="New Issue Submission")
    await interaction.response.send_modal(modal)


@client.tree.command(
    name="create-quick-project",
    description="create a new project with a channel and a webhook",
)
async def create_project_quickstart(
    interaction: discord.Interaction,
    name: str,
):
    channel = await interaction.guild.create_text_channel(name.replace(" ", "-"))
    webhook = await channel.create_webhook(
        name=client.user.name,
    )

    await interaction.response.send_message(
        " project created with <#{channel.id}> and created webhook"
    )


@client.tree.command(
    name="create-project",
    description="create a new project with a channel used as an issue feed",
)
async def create_project(
    interaction: discord.Interaction,
    name: str,
):
    # put req and add project name without creating a channel or webhook

    await interaction.response.send_message(f"created project {name}")


@client.tree.command(
    name="create-quick-issue-feed",
    description="create a new issue tracker channel with webhook",
)
async def create_issue_feed_quickstart(
    interaction: discord.Interaction,
    channel_name: str,
):
    channel = await interaction.guild.create_text_channel(
        channel_name.replace(" ", "-")
    )
    webhook = await channel.create_webhook(
        name=client.user.name,
    )

    await interaction.response.send_message(f"created <#{channel.id}> with a webhook")


@client.tree.command(
    name="issue-feed",
    description="use an existing channel for the issue feed",
)
async def create_issue_feed(
    interaction: discord.Interaction,
    channel_id: str,
):
    channel = await interaction.guild.fetch_channel(channel_id)
    webhook = await channel.create_webhook(
        name=client.user.name,
    )

    await interaction.response.send_message(f"created webhook in<#{channel.id}>")


@client.tree.command(
    name="add-contributors",
    description="add contributors to your project, you can add multiple ids separated by commas",
)
async def add_contributors(
    interaction: discord.Interaction,
    project: str,
    user_id: str,
):
    # find the project
    contributors_to_add = user_id.split(",")
    # then add the contributors

    if len(contributors_to_add) == 1:
        await interaction.response.send_message(f"added contributor")
    elif len(contributors_to_add) > 1:
        await interaction.response.send_message(
            f"added {len(contributors_to_add)} contributors"
        )


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command(name="hello")
async def say_hello(ctx):
    await ctx.send("hello")


# async def load_cogs():
#     for filename in os.listdir("./src/ticketing_system/bot/cogs"):
#         if filename.endswith(".py"):
#             await client.load_extension(f"{filename[:-3]}")


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
