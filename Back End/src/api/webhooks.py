import discord
from discord import Color




IGNORED_UPDATE_EVENT_KEYS = ["modLogs", "description", "attachments"]
webhook = discord.SyncWebhook.from_url("url")

def create_embed(message, color, title):
        return discord.Embed(title=title, description=message, color=color)

def send_new_issue(issue):
        title = "New Issue Created"
        color = str
        if issue['type'] == "bug":
                color = Color.red()
        else: 
                color = Color.yellow()

        message = f"""
        Type: {issue['type']}
        Category: {issue['category']}
        Summary: {issue['summary']}
        Version: {issue['version']}
        Player Name: {issue['playerName']}
        """
        embed = create_embed(title, message,  color)
        webhook.send(embed=embed)

def send_update_issue(diff):
        title = "Issue Updated"
        color = Color.green()
        ignored_update_list = []
        message_list = []

        for i in diff:
                if i['key'] in IGNORED_UPDATE_EVENT_KEYS:
                        ignored_update_list.append(i['key'])
                else:
                        message_list.append(f"{i['key']} : {i['old']} => {i['new']}\n")
        
        message= f'{"".join(message_list)}{", ".join(ignored_update_list)} updated, see website for details'
        embed = create_embed(title=title, message=message, color=color)
        webhook.send(embed=embed)
        






# def send_messages(project_id, message):
#     webhook_urls = db.webhooks.find({"project_id": project_id})
#     for url in webhook_urls:
        
#         webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1075163825990553712/n_Ro5J1uHx64yfFQ6MBov-CJzaRrCOC0L6s7t0xjD82fSd7D9K56sq7O7c46FHXnb0ZZ")
#         webhook = discord.SyncWebhook.from_url(url)
#         webhook.send(message)