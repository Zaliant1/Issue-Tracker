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

    @app_commands.command(
        name="create-project",
        description="create a new project with a channel used as an issue feed",
    )
    async def create_project(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        new_project = {
            "name": name,
            "author": interaction.user.id,
            "contributors": [],
        }
        if new_project["name"].replace(" ", "").isalnum():
            new_project["name"] = new_project["name"].replace(" ", "-")

            response = requests.put(
                "http://localhost:8000/api/project",
                json=new_project,
            )

            if response.status_code == 200:
                response = response.json()
                embed = discord.Embed(
                    title="Project Created!",
                    description=f"You can go [here](http://localhost:3000/project/{new_project['name']}) to see your newly created project",
                    color=Color.blurple(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await interaction.response.send_message(
                f"Project name {name} must be alphanumeric, spaces are accepted",
                ephemeral=True,
            )

    @app_commands.command(
        name="setup-project",
        description="create a new project with a channel and a webhook",
    )
    async def create_project_quickstart(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        new_project = {
            "name": name,
            "author": interaction.user.id,
            "contributors": [],
        }
        if new_project["name"].replace(" ", "").isalnum():
            new_project["name"] = new_project["name"].replace(" ", "-")

            response = requests.put(
                "http://localhost:8000/api/project",
                json=new_project,
            )

            if response.status_code == 200:
                channel = await interaction.guild.create_text_channel(
                    name.replace(" ", "-")
                )
                webhook = await channel.create_webhook(
                    name=interaction.client.user.name
                )

                new_webhook = {
                    "project_name": str(name),
                    "url": str(webhook.url),
                    "guild_id": str(webhook.guild_id),
                    "channel_": str(webhook.channel),
                    "channel_id": str(webhook.channel_id),
                    "categories": [],
                }

                response_webhooks = requests.put(
                    "http://localhost:8000/api/project/webhooks",
                    json=new_webhook,
                )

                if response_webhooks.status_code == 200:
                    embed = discord.Embed(
                        title="Project Created!",
                        description=f"Project created with <#{channel.id}> with webhook in channel, You can go [here](http://localhost:3000/project/{new_project['name']}) to see your newly created project",
                        color=Color.blurple(),
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"created project, channels, and webhook, but had an issue writing the webhook to the database {response_webhooks.status_code}",
                        ephemeral=True,
                    )
            else:
                await interaction.response.send_message(
                    response.status_code, ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"Project name {name} must be alphanumeric, spaces are accepted",
                ephemeral=True,
            )

    @app_commands.command(
        name="register-issue-feed",
        description="Will create webhook for issue feed on the specified project to the channel the command is run in.",
    )
    async def create_issue_feed(
        self,
        interaction: discord.Interaction,
        project_name: str,
    ):
        webhook = await interaction.channel.create_webhook(
            name=interaction.client.user.name
        )

        new_webhook = {
            "project_name": str(project_name),
            "url": str(webhook.url),
            "guild_id": str(webhook.guild_id),
            "channel_": str(webhook.channel),
            "channel_id": str(webhook.channel_id),
            "categories": [],
        }

        response_webhooks = requests.put(
            "http://localhost:8000/api/project/webhooks",
            json=new_webhook,
        )

        if response_webhooks.status_code == 200:
            embed = discord.Embed(
                title="Project Created!",
                description="Webhook for issue feed created in current channel",
                color=Color.blurple(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                f"created webhook, but had an issue writing the webhook to the database {response_webhooks.status_code}",
                ephemeral=True,
            )

    @app_commands.command(
        name="add-contributors",
        description="add a contributor to your project",
    )
    async def add_contributors(
        self,
        interaction: discord.Interaction,
        project_name: str,
        user_id: str,
    ):
        ##get username
        data = {"project_name": project_name, "user_id": user_id}
        response = requests.post(
            "http://localhost:8000/api/project/contributors",
            json=data,
        )

        if response.status_code == 200:
            embed = discord.Embed(
                title="Contributor Added!",
                description=f"<@{user_id}> added as contributor to {project_name}",
                color=Color.blurple(),
            )
            await interaction.response.send_message(embed=embed)


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
