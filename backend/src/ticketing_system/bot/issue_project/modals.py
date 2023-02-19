import requests
import discord
from discord import ui, Color


class NewIssue(ui.Modal):
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

    summary = ui.TextInput(
        label="summary",
        placeholder="Issue Summary",
        style=discord.TextStyle.paragraph,
    )
    issue: dict

    def __init__(self, project_id: int, issue_type: str, user_id: str, *args, **kwargs):
        self.project_id = project_id
        self.issue_type = issue_type
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction):
        new_issue = {
            "status": "reported",
            "summary": self.summary.value,
            "category": self.category.value,
            "type": self.issue_type,
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
            "project_id": self.project_id,
            "user_id": self.user_id,
        }

        response = requests.put(
            "http://localhost:8000/api/issue",
            json=new_issue,
        )

        if response.status_code == 200:
            response = response.json()

            embed = discord.Embed(
                title="Issue Created!",
                description=f"You can go [here](http://localhost:3000/issue/{response}) to fill out modlogs, attachments, and description",
                color=Color.blurple(),
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                error_message = response.json()["detail"]
            except:
                error_message = response.text

            await interaction.response.send_message(
                f"Unable to create issue!\n**Status:** {response.status_code}\n**Response:** {error_message}",
                ephemeral=True,
            )
