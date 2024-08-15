import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands

class SendNotification(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None
    
    @discord.ui.button(label = "Notify Users", style=discord.ButtonStyle.green)
    async def notifiy(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(view=self)
        successembed = discord.Embed(title=":white_check_mark: | Success",description=f"This channel has been unlocked by ``{interaction.user}``",color=discord.colour.parse_hex_number("00EF1E"))
        successembed.timestamp = datetime.now()
        await interaction.channel.send(embed = successembed)

class Unlock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Unlock a channel for a specific role.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction:discord.Interaction, role: discord.Role = None):
        channel = interaction.channel
        overwrites = channel.overwrites  # Fetch existing permissions
        
        if role != None:
            successembed = discord.Embed(title=":white_check_mark: | Success",description=f"Succesfully unlocked the channel for {role.mention}",color=discord.colour.parse_hex_number("00EF1E"))
            overwrite = overwrites.get(role, discord.PermissionOverwrite())
            overwrite.send_messages = True
            overwrites[role] = overwrite
            await channel.edit(overwrites=overwrites)
            await interaction.response.send_message(embed=successembed, ephemeral = True, view = SendNotification())
        else:
            successembed = discord.Embed(title=":white_check_mark: | Success",description=f"Succesfully unlocked the channel for @everyone",color=discord.colour.parse_hex_number("00EF1E"))
            overwrite = overwrites.get(interaction.guild.default_role, discord.PermissionOverwrite())
            overwrite.send_messages = True
            overwrites[interaction.guild.default_role] = overwrite
            await channel.edit(overwrites=overwrites)
            await interaction.response.send_message(embed=successembed, ephemeral = True, view = SendNotification())

    @unlock.error
    async def lock_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occured: {error}", ephemeral=True)

async def setup(client):
    await client.add_cog(Unlock(client))