import discord
from discord import SyncWebhook
from discord.ext import commands
from discord import app_commands



class Report(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(description = "Report a user for malicious activities.")
    @app_commands.describe(username = "The name of the user you want to report", user_id = "The id of the user you want to report", reason = "What did the user you want to report do wrong?")
    async def report(self, interaction:discord.Interaction, username:str, user_id:int, reason: str):
    
        embed = discord.Embed(title="Bot Report", description=f"**Username:** ```{username}```\n**User ID:** ```{user_id}```\n**Reason:** ```{reason}```", color=discord.Colour.orange())

        webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1157688987276804146/oPWvm1yw8_rAZY45hSA7MhaFzqKjeJVyi__qjJObf8RSdbfxtSvfiwLxd3HI06CM-_cK")

        webhook.send(embed=embed)

        await interaction.response.send_message(f"Report submitted for ``{username}`` with user ID ``{user_id}`` for the reason: ``{reason}``", ephemeral=True) 


async def setup(client):
    await client.add_cog(Report(client))