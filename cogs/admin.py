import discord
import asyncio
from discord.ext import commands
from discord import app_commands

class AdminTools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description = "Shows the server the bot is in.", aliases = ["ss", "sservers", "showser"])
    async def show_servers(self, ctx, invite:bool=False):
        if invite == True:
            guildlist = discord.Embed(title="Servers I'm in:", description="", color=discord.colour.parse_hex_number("6433FF"))
            for guild in self.client.guilds:
                invite = await guild.text_channels[0].create_invite()
                guildlist.add_field(name = f"Name: `{guild.name}`", value=f"**ID:** `{guild.id}`\n**Membercount:** `{guild.member_count}`\n**Boosts:** `{guild.premium_subscription_count}`\n**Roles:** `{len(guild.roles)}`\n**Invite:** [invite]({invite})", inline = True)
            await ctx.send(embed = guildlist)
        else:
            guildlist = discord.Embed(title="Servers I'm in:", description="", color=discord.colour.parse_hex_number("6433FF"))
            for guild in self.client.guilds:
                guildlist.add_field(name = f"Name: `{guild.name}`", value=f"**ID:** `{guild.id}`\n**Membercount:** `{guild.member_count}`\n**Boosts:** `{guild.premium_subscription_count}`\n**Roles:** `{len(guild.roles)}`", inline = True)
            await ctx.send(embed = guildlist)


async def setup(client):
    await client.add_cog(AdminTools(client))