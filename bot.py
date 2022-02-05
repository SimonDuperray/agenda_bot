from plistlib import load
import discord
from discord.ext import commands, tasks
import os
import dotenv
from dotenv import load_dotenv
import time, json

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="#", intents=intents)

@bot.event
async def on_ready():
    print("> Bot connected")

@bot.command(name="disconnect", help="Disconnect the bot from the server")
async def disconnect(ctx):
    await ctx.send("I have to go. Bye!")
    await client.close()

@bot.command(name="hello", help="my first command")
async def hello(ctx):
    await ctx.send("Hi !")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)