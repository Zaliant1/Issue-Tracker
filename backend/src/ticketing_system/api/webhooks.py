import discord
import os
from discord import Color
from dotenv import load_dotenv

load_dotenv()

IGNORED_UPDATE_EVENT_KEYS = ["modLogs", "description", "attachments"]
webhook = discord.SyncWebhook.from_url(os.environ.get("WEBHOOK_URL"))


def create_embed(message, color, title):
    return discord.Embed(title=title, description=message, color=color)


def embed_test():
    embed = create_embed(title="hi", message="this is a test", color=Color.green())
    webhook.send("asdfasdf", embed=embed)


def create_new_issue_embed(issue):
    color = str
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


def send_update_issue(diff):
    title = "Issue Updated"
    ignored_update_list = []
    message_list = []

    for i in diff:
        if i["key"] in IGNORED_UPDATE_EVENT_KEYS:
            ignored_update_list.append(i["key"])
        else:
            message_list.append(f"{i['key']} : {i['old']} => {i['new']}\n")
    if len(ignored_update_list) > 0:
        message = f'{"".join(message_list)}{", ".join(ignored_update_list)} updated, see website for details'

    elif len(ignored_update_list) == 0:
        message = f'{"".join(message_list)}'

    embed = create_embed(title=title, message=message, color=Color.blue())
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


# def send_messages(project_id, message):
#     webhook_urls = db.webhooks.find({"project_id": project_id})
#     for url in webhook_urls:

#         webhook = discord.SyncWebhook.from_url(url)
#         webhook.send(message)
