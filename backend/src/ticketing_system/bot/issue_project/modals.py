import requests
import discord
from discord import ui, Color


class NewIssue(ui.Modal):
    issue: dict

    category = ui.TextInput(
        label="category",
    )

    version = ui.TextInput(
        label="version",
        placeholder="Version",
    )

    summary = ui.TextInput(label="summary", placeholder="Summary")

    description = ui.TextInput(
        label="description",
        placeholder="Description",
        style=discord.TextStyle.paragraph,
    )

    def __init__(
        self,
        project_name: str,
        issue_type: str,
        user_id: str,
        priority: str,
        *args,
        **kwargs,
    ):
        self.project_name = project_name
        self.issue_type = issue_type
        self.user_id = user_id
        self.priority = priority

        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction):
        new_issue = {
            "status": "reported",
            "summary": self.summary.value,
            "category": self.category.value,
            "type": self.issue_type,
            "priority": self.priority,
            "version": self.version.value,
            "description": self.description.value,
            "modlogs": {
                "title": "",
                "body": "",
            },
            "archived": False,
            "attachments": {"embed_source": "", "general_url": ""},
            "project_name": self.project_name,
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
                description=f"You can go [here](http://localhost:3000/issue/{response}) to fill submit modlogs and add  attachments",
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
