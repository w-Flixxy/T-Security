import discord
import datetime
from discord.ext import commands

class OnJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
            entry_user = entry.user
            entry_user_id = entry_user.id

        with open("T-Security/reported_users.txt", "r") as f:
            content = f.read()
            reported_users = content.splitlines()

        if str(member.id) in reported_users:
            try:
                member.kick()
                danger_embed = discord.Embed(title="A user that has been flagged by our systems joined your server!",description="", colour=discord.colour.parse_hex_number("E70000"))
                danger_embed.add_field(name="User info:",value=f"Name: ``{member}``\nID: ``{member.id}``\n\nAdded by: ``{entry_user}``\nID: ``{entry_user_id}``")
                danger_embed.add_field(name="", value="\n\n_The user who added the bot has been timed out for 1 day and had their roles removed._",inline=False)
                danger_embed.set_thumbnail(url=member.display_avatar.url)
                message = await guild.owner.send(embed=danger_embed)
                for role in entry_user.roles:
                    if role.name == "@everyone":
                        pass
                    else:
                        await entry_user.remove_roles(role)
                timeout_duration = datetime.timedelta(days=1)
                timeout_expiration = datetime.datetime.now().astimezone() + timeout_duration
                await entry_user.timeout(timeout_expiration)

            except discord.Forbidden:
                await member.kick()
                danger_embed = discord.Embed(title="A user that has been flagged by our systems joined your server!",description="", colour=discord.colour.parse_hex_number("E70000"))
                danger_embed.add_field(name="User info:",value=f"Name: ``{member}``\nID: ``{member.id}``\n\nAdded by: ``{entry_user}``\nID: ``{entry_user_id}``")
                danger_embed.add_field(name="", value="\n\n~~_The user who added the bot has been timed out for 1 day and had their roles removed._~~",inline=False)
                danger_embed.set_thumbnail(url=member.display_avatar.url)
                danger_embed.add_field(name="Failed to timeout user!", value="Missing permission!")
                await message.edit(embed=danger_embed)


async def setup(client):
    await client.add_cog(OnJoin(client))
