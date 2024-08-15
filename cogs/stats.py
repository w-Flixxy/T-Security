import discord
from discord import app_commands
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @app_commands.command(description="Recieve more information about the server", name = "teststats")
    @app_commands.describe(scope = "The item you want more information about.")
    @app_commands.choices(
    scope=[
        app_commands.Choice(name="Server", value="server"),
        app_commands.Choice(name="Membercount", value="membercount"),
        app_commands.Choice(name="Channels", value="channels"),
        app_commands.Choice(name="General info",value="general")])
    async def test(self, interaction: discord.Interaction, scope: app_commands.Choice[str]):
        print(f"{scope}, {scope}, {scope}")
        if scope.value == "Server":
            server_embed = discord.Embed(title = "More server stats:", description="", colour = discord.colour.parse_hex_number("4344FF"))
            server_embed.add_field(name="Server Name:", value = f"{interaction.guild.name}", inline = False)
            server_embed.add_field(name="Server description:", value = f"{interaction.guild.description}", inline = False)
            server_embed.add_field(name="Server ID:", value = f"{interaction.guild.id}", inline = False)
            server_embed.add_field(name="Server owner:", value = f"{interaction.guild.owner}", inline = False)
            server_embed.add_field(name="Server icon url:", value = f"``{interaction.guild.icon}``", inline = False)
            server_embed.add_field(name="Server AFK channel:", value = f"{interaction.guild.afk_channel}", inline = False)
            server_embed.set_thumbnail(url = interaction.guild.icon)
            await interaction.response.send_message(embed = server_embed, ephemeral=True)
        if scope.name == "Membercount":
            non_bot_count = sum(1 for member in interaction.guild.members if not member.bot)
            bot_count = len(interaction.guild.members) - non_bot_count
            member_info = discord.Embed(title="Member info", description="", color=discord.colour.parse_hex_number("4344FF"))
            member_info.add_field(name="Humans:", value = f"{non_bot_count}", inline = False)
            member_info.add_field(name="Bots:", value = f"{bot_count}", inline = False)
            member_info.set_thumbnail(url = interaction.guild.icon)
            await interaction.response.send_message(embed = member_info, ephemeral=True)
        if scope.name == "Channels":
            channels_info = discord.Embed(title="Channels", description="", color=discord.colour.parse_hex_number("4344FF"))
            channels_info.add_field(name="Total channels:", value=f"{len(interaction.guild.channels)}", inline = False)
            channels_info.add_field(name="Text channels:", value=f"{len(interaction.guild.text_channels)}", inline = False)
            channels_info.add_field(name="Voice channels:", value=f"{len(interaction.guild.voice_channels)}", inline = False)
            channels_info.add_field(name="Other channels", value=f"{len(interaction.guild.channels) - len(interaction.guild.text_channels) - len(interaction.guild.voice_channels)}", inline=False)
            await interaction.response.send_message(embed = channels_info, ephemeral=True)
        if scope.value == "general":
            stats_embed = discord.Embed(title="Server stats", description="", color = discord.colour.parse_hex_number("4344FF"))
            stats_embed.add_field(name = "Servername:", value = f"{interaction.guild.name}", inline = True)
            stats_embed.add_field(name = "Membercount:", value = f"{len(interaction.guild.members)}", inline = True)
            stats_embed.add_field(name = "Total channels:", value = f"{len(interaction.guild.channels)}", inline = False)
            stats_embed.set_thumbnail(url = interaction.guild.icon)
            await interaction.response.send_message(embed = stats_embed, ephemeral=True)

async def setup(client):
    await client.add_cog(Stats(client))