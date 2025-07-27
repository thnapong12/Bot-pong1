import os
import discord
from discord.ext import commands
import asyncio

from myserver import server_on

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ADMIN_CHANNEL_ID = 1397786254120325192
ROLE_ID = 1394664390741069864

@bot.event
async def on_ready():
    print("Online")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        return

    message = await channel.send(
        f"{member.mention} joined the server.\nApprove?\n✅ = Yes | ❌ = No"
    )

    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reac, usr):
        return (
            usr.guild_permissions.administrator and
            reac.message.id == message.id and
            str(reac.emoji) in ["✅", "❌"]
        )

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        if str(reaction.emoji) == "✅":
            role = member.guild.get_role(ROLE_ID)
            if role:
                await member.add_roles(role)
                await channel.send(f"{member.mention} ได้รับยศแล้ว ✅")
            else:
                await channel.send("ไม่พบ Role ตาม ID ที่กำหนด ❗")
        else:
            await member.kick(reason="Not approved")
            await channel.send(f"{member.name} ถูกเตะออก ❌")
    except asyncio.TimeoutError:
        await channel.send(f"ไม่มีใครตอบ {member.mention} ภายในเวลา ⏰")


server_on()

bot.run(os.getenv("TOKEN"))