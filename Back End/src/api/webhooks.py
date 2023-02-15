import discord


def send_new_issue(message):
        webhook = discord.SyncWebhook.from_url("fake_url_for_pushing")
        embed=discord.Embed(title="New Issue Created", description=message, color=0x00ff40)
        webhook.send(embed=embed)


# def send_messages(project_id, message):
#     webhook_urls = db.webhooks.find({"project_id": project_id})
#     for url in webhook_urls:
        
#         webhook = discord.SyncWebhook.from_url(url)
#         webhook.send(message)