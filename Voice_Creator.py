import discord
from discord.ext import commands
import asyncio

"""
This program will make the bot create a voice channel
    each time a new user join the #Temporary voice channel
"""

intents = discord.Intents.default()
intents.voice_states = True  # Enable voice state tracking
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Name of the channel
TEMP_CHANNEL_NAME = "Temporary"

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the member joined the temporary channel
    guild = member.guild

    if after.channel and after.channel.name == TEMP_CHANNEL_NAME:
        # Create a new voice channel
        category = after.channel.category
        temp_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Channel",
            category=category
        )

        # move the member to the voice channel
        await member.move_to(temp_channel)

        # check for update and remove the channel if empty
        await check_and_delete_channel(temp_channel)
    
async def check_and_delete_channel(channel):
    await bot.wait_until_ready()

    while True:
        if len(channel.members) == 0:
            await channel.delete()
            break
        await asyncio.sleep(5)

bot.run("Token")