import discord
from discord import app_commands
from discord.ext import commands



class Addrole(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @app_commands.command(name="addrole", description = "Adds a role to a specific user.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(self, interaction: discord.Interaction, role:discord.Role, user:discord.Member):
        print(interaction.user.roles)
        userroles = interaction.user.roles
        highest_role = userroles[-1]
        print(highest_role)
        highest_role_position = interaction.guild.roles.index(highest_role)
        print(highest_role_position)
        position_given_role = interaction.guild.roles.index(role)
        if position_given_role >= highest_role_position:
            fail_embed = discord.Embed(title=":x: | Failed", colour = discord.colour.parse_hex_number("4344FF"))
            fail_embed.add_field(value = f"You cannot give roles higher or equal to your highest role!", name = "")
            await interaction.response.send_message(embed = fail_embed ,ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            success_embed = discord.Embed(title=":white_check_mark: | Success", colour = discord.colour.parse_hex_number("4344FF"))
            success_embed.add_field(value = f"Succesfully given {role.mention} to {user.mention}.", name = "")
            await interaction.response.send_message(embed = success_embed, ephemeral = True)
    @addrole.error
    async def addrole_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            error_embed = discord.Embed(title = ":x: | An error occured.", colour=discord.colour.parse_hex_number("4344FF"))
            error_embed.add_field(name = "", value = f"```{error}```")
            await interaction.response.send_message(embed = error_embed, ephemeral=True)


async def setup(client):
    await client.add_cog(Addrole(client))