import requests
import discord
from discord import app_commands, Color
from discord.ext import commands


from .modals import NewIssue


class IssueProject(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

    @commands.command(name="risto")
    async def risto(self, ctx: commands.Context) -> None:
        await ctx.send(
            "https://cdn.discordapp.com/attachments/825530277694144542/1077734017790656583/image.png"
        )

    # Adds an issue
    @app_commands.command(name="add-issue")
    @app_commands.describe(
        project_name="name of the project you want to register issue feed for",
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
        project_name: str,
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
            project_name=project_name,
            issue_type=issue_type.name.lower(),
            user_id=interaction.user.id,
            priority=priority.name.lower(),
        )
        modal.category.placeholder = " | ".join(categories)
        await interaction.response.send_modal(modal)

    # Create a new project and add the message author as a contributor to the new project.
    # Associates the discord guild with a project_name
    @app_commands.command(
        name="create-project",
        description="Create a new project and add the message author as a contributor to the new project.",
    )
    async def create_project(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        project, has_error = self._create_project_api(name, interaction.user.id)
        if not has_error:
            embed = discord.Embed(
                title="Project Created!",
                description=f"You can go [here](http://localhost:3000/project/{name}) to see your newly created project",
                color=Color.blurple(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if project:
                await interaction.response.send_message(
                    "Error creating project",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Project name {name} must be alphanumeric, spaces are accepted",
                    ephemeral=True,
                )

    # Creates a new project with message author as a contributor.
    # Creates a new channel with the specified project name.
    # Creates a webhook on the newly created channel for issue feed
    @app_commands.command(
        name="setup-project",
        description="create a new project with a channel and a webhook",
    )
    async def create_project_quickstart(
        self,
        interaction: discord.Interaction,
        name: str,
    ):
        project, has_error = self._create_project_api(name, interaction.user.id)
        if not has_error:
            await self._webhook_setup_api(project["project_name"], interaction)
        else:
            if project:
                await interaction.response.send_message(
                    "Error creating project", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"Project name {name} must be alphanumeric, spaces are accepted",
                    ephemeral=True,
                )

    # Will create webhook for issue feed on the specified project to the channel the command is run in.
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

    # Associates a contributor to a project and will provide additional access to issue site
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
        data = {"project_name": project_name, "user_id": user_id}
        response = requests.post(
            "http://localhost:8000/api/project/contributors",
            json=data,
        )

        if response.status_code == 200:
            user_info = {
                "user_id": user_id,
                "projects": [{project_name: "contributor"}],
            }

            user_response = requests.put(
                "http://localhost:8000/api/user/create",
                json=user_info,
            )

            if user_response.status_code == 200:
                embed = discord.Embed(
                    title="Contributor Added!",
                    description=f"<@{user_id}> added as a contributor to {project_name}",
                    color=Color.blurple(),
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="add-categories", description="description")
    @app_commands.describe(
        name="name of the project you want to register categories for",
        categories="The categories for your issues, add multiple seperated by commas",
    )
    async def add_categories(
        self,
        interaction: discord.Interaction,
        name: str,
        categories: str,
    ):
        new_categories = categories.split(",")

        response = requests.put(
            f"http://localhost:8000/api/project/{name}/categories", json=new_categories
        )

        if response.status_code == 200:
            embed = discord.Embed(
                title="Categories Added!",
                description=f"added categories to {name}: {new_categories}",
                color=Color.blurple(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await interaction.response.send_message(
                f"couldn't create categories",
                ephemeral=True,
            )

    def _create_project_api(self, name, user_id):
        new_project = {
            "name": name,
            "author": user_id,
            "contributors": [],
            "categories": [],
        }
        has_error = True
        if new_project["name"].replace(" ", "").isalnum():
            new_project["name"] = new_project["name"].replace(" ", "-")

            response = requests.put(
                "http://localhost:8000/api/project",
                json=new_project,
            )

            if response.status_code == 200:
                return response.json(), False

            return response.status_code, has_error

        return None, has_error

    async def _webhook_setup_api(self, project_name, interaction):
        channel = await interaction.guild.create_text_channel(project_name)
        webhook = await channel.create_webhook(name=interaction.client.user.name)

        new_webhook = {
            "project_name": project_name,
            "url": str(webhook.url),
            "guild_id": str(webhook.guild_id),
            "channel_": str(webhook.channel),
            "channel_id": str(webhook.channel_id),
        }

        response = requests.put(
            "http://localhost:8000/api/project/webhooks",
            json=new_webhook,
        )

        if response.status_code == 200:
            embed = discord.Embed(
                title="Project Created!",
                description=f"Project created with <#{channel.id}> with webhook in channel, You can go [here](http://localhost:3000/project/{project_name}) to see your newly created project",
                color=Color.blurple(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                f"created project, channels, and webhook, but had an issue writing the webhook to the database {response.status_code}",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(IssueProject(bot=bot))
    print("cog added")
