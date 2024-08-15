import os
import discord
import time
import json
from flask import Flask
from threading import Thread
from discord import SyncWebhook
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from help_command import help_command



with open("T-Security/token.txt", "r")as f:
    token = f.read()
f.close()

client = commands.Bot(command_prefix=["t!","-"], intents=discord.Intents.all(), help_command=help_command())

@client.command()
@commands.is_owner()
async def sync(ctx):
    await client.tree.sync()
    await ctx.send("Succesfully synced slash commands!")

@client.event
async def on_slash_command_error(self, interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You do not have permission to use this command.")
    else:
        await interaction.response.send_message(f"{error}")

channel_creation_times = {}
channel_deletion_times = {}

nopermemb=discord.Embed(title = ":x: | Missing permission!",description = "I'm missing permission to execute this command!", colour = discord.colour.parse_hex_number("F20000"))

username = "your username here"

@client.tree.command(name="purge", description="Removes the given ammount of messages")
@app_commands.checks.has_permissions(manage_messages = True)
@app_commands.describe(amount="How much messages should be purged?")
async def purge_command(interaction: discord.Interaction, amount:int):
    await interaction.response.send_message(f"Trying to purge {amount} message(s)!", ephemeral=True)
    await interaction.channel.purge(limit=amount)
    succesembed = discord.Embed(title=":white_check_mark: | Success", description=f"Succesfully purged {amount} message(s)!", colour = discord.colour.parse_hex_number("09D330"))
    await interaction.channel.send(embed = succesembed, delete_after=4)

@purge_command.error
async def test_error(interaction : discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.channel.send(embed=nopermemb, ephemeral=True, delete_after=4)
    else :
        errorembed = discord.Embed(title="There was an error running the command!", description="")
        errorembed.add_field(name="ERROR", value=f"Please contact the developer ``{username}``! \nThe error is:{error}")
        await interaction.channel.send(embed=errorembed,ephemeral=True, delete_after=4)

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print(client.user)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(client.guilds)} servers!"))
    for filename in os.listdir("T-Security/cogs"):
        print(filename)
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_guild_channel_create(channel):
    file_path = "T-Security/preferences.json"
    key = str(channel.guild.id)
    with open(file_path, 'r') as file:
            data = json.load(file)
        
    # Check if the key exists and is a boolean
    if key in data:
        if data[key]:
            pass
        else:
            return
    else:
        data[key] = True
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                    creator = entry.user
    user_id = creator.id  # You can change this to get the user ID from the channel creator
    if user_id not in channel_creation_times:
        channel_creation_times[user_id] = []

    channel_creation_times[user_id].append(datetime.now())

    # Check if the user has created channels rapidly
    if len(channel_creation_times[user_id]) >= 5:  # Change the threshold as per your requirement
        time_difference = channel_creation_times[user_id][-1] - channel_creation_times[user_id][-3]
        if time_difference.total_seconds() <= 10:
            guild = channel.guild
            user = guild.get_member(user_id)
            if user:
                await creator.kick(reason="Creating channels rapidly")

@client.event
async def on_guild_channel_delete(channel):
    file_path = "T-Security/preferences.json"
    key = str(channel.guild.id)
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    # Check if the key exists and is a boolean
    if key in data:
        if data[key]:
            pass
        else:
            return
    else:
        data[key] = True
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                    creator = entry.user
    user_id = creator.id  # You can change this to get the user ID from the channel creator
    if user_id not in channel_deletion_times:
        channel_deletion_times[user_id] = []

    channel_deletion_times[user_id].append(datetime.now())

    # Check if the user has created channels rapidly
    if len(channel_deletion_times[user_id]) >= 5:  # Change the threshold as per your requirement
        time_difference = channel_deletion_times[user_id][-1] - channel_deletion_times[user_id][-3]
        if time_difference.total_seconds() <= 5:
            guild = channel.guild
            user = guild.get_member(user_id)
            if user:
                await creator.kick(reason="Deleting channels rapidly")

@commands.is_owner()
@client.command()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    print(f"Loaded: cogs.{extension}")
    await ctx.send(f"Succesfully loaded `cogs.{extension}`!")

@commands.is_owner()
@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    print(f"Unloaded: cogs.{extension}")
    await ctx.send(f"Succesfully unloaded `cogs.{extension}`!")

@commands.is_owner()
@client.command(aliases=["rl"])
async def reload(ctx, extension):
    if extension == "all":
        for filename in os.listdir("T-Security/cogs"):
            if filename.endswith(".py"):
                await client.unload_extension(f"cogs.{filename[:-3]}")
        for filename in os.listdir("T-Security/cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("Succesfully reloaded all cog files.")
    else:
        await client.unload_extension(f"cogs.{extension}")
        await client.load_extension(f"cogs.{extension}")
        await ctx.send(f"Succesfully reloaded `cogs.{extension}`!")



reported_users=[]

@client.event
async def on_member_remove(member):
    guild = member.guild
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member and entry.reason == "Creating channels rapidly":
            owner = guild.owner
            raidembed=discord.Embed(title="We have detected a raid!",type="rich",description="",color=discord.Color.orange())
            raidembed.add_field(name="Watch out! Your server might be experiencing a raid!",value=f"No need to worry! We've already kicked the user!\n\nName:```{member.name}```\nID: ```{member.id}```")
            raidembed.add_field(name="The user has already been reported to the T-Security admins.",value="",inline=False)
            await owner.send(embed=raidembed)
            with open("T-Security/reported_users.txt","r") as f:
                content=f.read()
                for id in content.splitlines():
                    reported_users.append(entry.target.id)
                print(reported_users)
                if f"{entry.target.id}" in reported_users:
                    print(f"{entry.target.name} is already reported!")
                    f.close()
                else:
                    with open("T-Security/reported_users.txt","a") as f:
                        f.write(f"\n{entry.target.id}")
                    f.close()
    
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member and entry.reason == "Deleting channels rapidly":
            owner = guild.owner
            raidembed=discord.Embed(title="We have detected a raid!",type="rich",description="",color=discord.Color.orange())
            raidembed.add_field(name="Watch out! Your server might be experiencing a raid!",value=f"No need to worry! We've already kicked the user!\n\nName:```{member.name}```\nID: ```{member.id}```")
            raidembed.add_field(name="The user has already been reported to the T-Security admins.",value="",inline=False)
            await owner.send(embed=raidembed)
            with open("T-Security/reported_users.txt","r") as f:
                content=f.read()
                for id in content.splitlines():
                    reported_users.append(entry.target.id)
                print(reported_users)
                if f"{entry.target.id}" in reported_users:
                    print(f"{entry.target.name} is already reported!")
                    f.close()
                else:
                    with open("T-Security/reported_users.txt","a") as f:
                        f.write(f"\n{entry.target.id}")
                    f.close()



def flaskserver():
    app = Flask(__name__)
    @app.route('/')
    def hello_world():
        return 'Hello World'
    
    # main driver function
    if __name__ == '__main__':
        app.run(port="8012", host = "0.0.0.0")

start_flask_server = Thread(target = flaskserver)
start_flask_server.start()

def start_bot():
    client.run(token)

start_bot()

