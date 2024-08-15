import json
import discord
from discord import SyncWebhook
from discord.ext import commands
from discord import app_commands

file_path = "T-Security/preferences.json"

def toggle_json_value(file_path, key):
    try:
        # Read the existing JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Check if the key exists and toggle its value, otherwise create it and set it to false
        if key in data:
            if isinstance(data[key], bool):
                data[key] = not data[key]
            else:
                print(f"The value of the key '{key}' is not a boolean.")
                return
        else:
            data[key] = False
            print(f"The key '{key}' did not exist and has been created with a value of False.")
        
        # Write the updated JSON data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Successfully toggled the value of '{key}' to {data[key]}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

class Preferences(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="This will enable/disable the raid protection.", name = "toggle-anti-raid")
    async def toggle_anti_raid(self, interaction:discord.Interaction):
        key = f"{interaction.guild.id}"

        toggle_json_value(file_path, f"{interaction.guild.id}")

        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if data[key]:
            enabled = discord.Embed(title="", description="Raid Protection enabled", color=discord.colour.parse_hex_number("4344FF"))
            enabled.add_field(name ="", value="Your server is now 24/7 protected by T-Securty against any raid attempts.")
            await interaction.response.send_message(embed = enabled, ephemeral=True)
        else:
            disabled = discord.Embed(title="", description="Raid Protection disabled", color=discord.colour.parse_hex_number("4344FF"))
            disabled.add_field(name ="", value="Your server is not protected against raid attempts, any raids that happen, wil not be shared.")
            await interaction.response.send_message(embed = disabled, ephemeral=True)
        
        

async def setup(client):
    await client.add_cog(Preferences(client))