import requests
import discord
from discord import app_commands, Color
from discord.ext import commands

from .modals import NewIssue


class IssueProject(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("issue project cog loaded")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.tree.copy_global_to(guild=guild)

    @commands.command(name="sync")
    async def sync(self, ctx) -> None:
        self.bot.tree.copy_global_to(guild=ctx.guild)
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands to the current guild")

    @commands.command(name="user-mention")
    async def user_mention(self, ctx: commands.Context) -> None:
        await ctx.send(f"<@{ctx.author.id}>")

    @app_commands.command(
        name="register-issue-feed",
        description="Will create webhook for issue feed on the specified project to the channel the command is run in.",
    )
    @app_commands.describe(
        project_id="id of the project you want to register issue feed for"
    )
    async def register_issue_feed(
        self, interaction: discord.Interaction, project_id: str
    ):
        await interaction.response.send_message(f"Issue feed registered!")

    @app_commands.command(name="add-issue")
    @app_commands.describe(
        project_id="id of the project you want to register issue feed for",
        issue_type="Either Bug or Suggestion",
    )
    @app_commands.choices(
        issue_type=[
            discord.app_commands.Choice(name="Bug", value=1),
            discord.app_commands.Choice(name="Suggestion", value=2),
        ]
    )
    @app_commands.choices(
        priority=[
            discord.app_commands.Choice(name="Low", value=1),
            discord.app_commands.Choice(name="Medium", value=2),
            discord.app_commands.Choice(name="High", value=3),
        ]
    )
    async def add_issue(
        self,
        interaction: discord.Interaction,
        project_id: int,
        issue_type: discord.app_commands.Choice[int],
        priority: discord.app_commands.Choice[int],
    ):
        categories = [
            "zemar",
            "dayya",
            "foobar",
        ]  # TODO: Change fetch api based on project ID

        modal = NewIssue(
            title="New Issue Submission",
            project_id=project_id,
            issue_type=issue_type.name.lower(),
            user_id=interaction.user.id,
            priority=priority.name.lower(),
        )
        modal.category.placeholder = " | ".join(categories)
        await interaction.response.send_modal(modal)


# @client.tree.command(
#     name="create-quick-project",
#     description="create a new project with a channel and a webhook",
# )
# async def create_project_quickstart(
#     interaction: discord.Interaction,
#     name: str,
# ):
#     channel = await interaction.guild.create_text_channel(name.replace(" ", "-"))
#     webhook = await channel.create_webhook(
#         name=client.user.name,
#     )

#     await interaction.response.send_message(
#         " project created with <#{channel.id}> and created webhook"
#     )


# @client.tree.command(
#     name="create-project",
#     description="create a new project with a channel used as an issue feed",
# )
# async def create_project(
#     interaction: discord.Interaction,
#     name: str,
# ):
#     # put req and add project name without creating a channel or webhook

#     await interaction.response.send_message(f"created project {name}")


# @client.tree.command(
#     name="create-quick-issue-feed",
#     description="create a new issue tracker channel with webhook",
# )
# async def create_issue_feed_quickstart(
#     interaction: discord.Interaction,
#     channel_name: str,
# ):
#     channel = await interaction.guild.create_text_channel(
#         channel_name.replace(" ", "-")
#     )
#     webhook = await channel.create_webhook(
#         name=client.user.name,
#     )

#     await interaction.response.send_message(f"created <#{channel.id}> with a webhook")


# @client.tree.command(
#     name="issue-feed",
#     description="use an existing channel for the issue feed",
# )
# async def create_issue_feed(
#     interaction: discord.Interaction,
#     channel_id: str,
# ):
#     channel = await interaction.guild.fetch_channel(channel_id)
#     webhook = await channel.create_webhook(
#         name=client.user.name,
#     )

#     await interaction.response.send_message(f"created webhook in <#{channel.id}>")


# @client.tree.command(
#     name="add-contributors",
#     description="add contributors to your project, you can add multiple ids separated by commas",
# )
# async def add_contributors(
#     interaction: discord.Interaction,
#     project: str,
#     user_id: str,
# ):
#     # find the project
#     contributors_to_add = user_id.split(",")
#     # then add the contributors

#     if len(contributors_to_add) == 1:
#         await interaction.response.send_message(f"added contributor")
#     elif len(contributors_to_add) > 1:
#         await interaction.response.send_message(
#             f"added {len(contributors_to_add)} contributors"
#         )
