import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="The help command")
    async def help(self, interaction:discord.Interaction):
        help_embed = discord.Embed(title = "Help Menu", description="All commands and their descriptions are listed below", colour = discord.colour.parse_hex_number("4344FF"))
        for command in self.client.tree.walk_commands():
            help_embed.add_field(name = command.name, value = command.description)
        await interaction.response.send_message(embed = help_embed)

async def setup(client):
    await client.add_cog(Help(client))