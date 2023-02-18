import discord
from discord import app_commands
from discord.ext import commands


class Color(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("color cog loaded")

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands to the current guild")
        return

    @app_commands.command(name="choosecolor", description="color selector")
    @app_commands.describe(colors="colors here")
    @app_commands.choices(
        colors=[
            discord.app_commands.Choice(name="red", value=1),
            discord.app_commands.Choice(name="green", value=2),
        ]
    )
    async def color_selector(
        interaction: discord.Interaction, colors: discord.app_commands.Choice[int]
    ):
        await interaction.response.send_message(f"color selected: {colors.name}")


async def setup(bot):
    await bot.add_cog(Color(bot), guilds=[discord.Object(id=636623317180088321)])
