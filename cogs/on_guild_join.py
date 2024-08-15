import discord
from discord import app_commands
from discord.ext import commands

class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(len(self.client.guilds))
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(self.client.guilds)} servers!"))

async def setup(client):
    await client.add_cog(OnGuildJoin(client))