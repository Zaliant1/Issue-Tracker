import discord
import os
from discord import Color
from dotenv import load_dotenv

load_dotenv()

IGNORED_UPDATE_EVENT_KEYS = ["modLogs", "description", "attachments"]
webhook = discord.SyncWebhook.from_url(os.getenv("WEBHOOK_URL"))
print(webhook)


def create_embed(message, color, title):
    return discord.Embed(title=title, description=message, color=color)


def create_new_issue_embed(issue):
    if issue["type"] == "bug":
        color = Color.red()
    else:
        color = Color.yellow()

    embed = discord.Embed(color=color)

    embed.add_field(name="Type", value=issue["type"], inline=False)
    embed.add_field(name="Category", value=issue["category"], inline=False)
    embed.add_field(name="Summary", value=issue["summary"], inline=False)
    embed.add_field(name="Version", value=issue["version"], inline=False)
    embed.add_field(name="Player", value=issue["playerName"], inline=False)

    return embed


def send_new_issue(issue):
    embed = create_new_issue_embed(issue)
    webhook.send("**New Issue Created**", embed=embed)


def send_update_issue(diff, issue_id):
    description = (
        f"[click here to see issue in website](http://localhost:3000/issue/{issue_id})"
    )
    ignored_update_list = []
    message_list = []
    embed = discord.Embed(
        title="Issue Updated!", description=description, color=Color.blurple()
    )

    for i in diff:
        if i["key"] in IGNORED_UPDATE_EVENT_KEYS:
            ignored_update_list.append(i["key"])
        else:
            message_list.append({f"{i['key']}": f"{i['old']} \u2b95 {i['new']}\n"})

    if len(ignored_update_list) > 0:
        for message in message_list:
            for k, v in message.items():
                if k == "summary":
                    embed.add_field(
                        name=k,
                        value=v,
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name=k,
                        value=v,
                        inline=True,
                    )
        embed.add_field(
            name="", value=f"{', '.join(ignored_update_list)} updated", inline=False
        )

        embed.set_footer(
            text="Description, Modlogs, and Attachments not shown, click above link to view"
        )
        webhook.send(embed=embed)

    elif len(ignored_update_list) == 0:
        for message in message_list:
            for k, v in message.items():
                if k == "summary":
                    embed.add_field(
                        name=k,
                        value=v,
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name=k,
                        value=v,
                        inline=True,
                    )
        embed.set_footer(
            text="Description, Modlogs, and Attachments not shown, click above link to view"
        )
        webhook.send(embed=embed)


def send_deleted_issue(issue):
    title = "Issue Deleted"
    color = Color.red()

    message = f"""
        Type: {issue['type']}
        Category: {issue['category']}
        Summary: {issue['summary']}
        Version: {issue['version']}
        Player Name: {issue['playerName']}
        """
    embed = create_embed(title=title, message=message, color=color)
    webhook.send(embed=embed)
