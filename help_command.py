import discord
from discord.ext import commands

class help_command(commands.HelpCommand):

    async def send_bot_help(self, mapping): 
        channel = self.get_destination()
        ctx = self.context
        author = ctx.author
        message = ctx.message
        embed = discord.Embed(color=discord.colour.parse_hex_number("4344FF"), title = "", description="Please use the slash command to recieve a list of all available commands")
        await ctx.message.reply(mention_author = False,embed = embed)



    async def send_command_help(self, command):

        channel = self.get_destination()
        ctx = self.context
        embed = discord.Embed(color=discord.colour.parse_hex_number("4344FF"), title = "", description="Please use the slash command to recieve a list of all available commands")
        await ctx.message.reply(mention_author = False,embed = embed)