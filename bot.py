import discord, json, os, datetime
from discord.ext import commands
from dotenv import load_dotenv
from plistlib import load
from rich import print
from stringcolor import *

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

@bot.command(name="dispo", help="Check availability")
async def dispo(ctx):
    availabilities = {
        "available": [],
        "unavailable": [],
    }
    now = datetime.datetime.now()

    with open('./data/agendas.json') as agendas:
        agendas = json.load(agendas)['agendas']

    for agenda in agendas:
        print(f"> {agenda['name']}")
        for lesson in agenda['agenda']:
            starth = int(lesson['Debut'][11:13])
            startm = int(lesson['Debut'][14:16])
            starts = int(lesson['Debut'][17:19])
            endh = int(lesson['Fin'][11:13])
            endm = int(lesson['Fin'][14:16])
            ends = int(lesson['Fin'][17:19])
            
            start=now.replace(hour=starth, minute=startm, second=starts, microsecond=0)
            end=now.replace(hour=endh, minute=endm, second=ends, microsecond=0)

            # if available...
            if(start<now and end>now):
                if agenda['name'] not in availabilities['unavailable']:
                    availabilities['unavailable'].append(agenda['name'])
            else:
                if agenda['name'] not in availabilities['available']:
                    availabilities['available'].append(agenda['name'])

    # create embedded message
    av_label = "Available"
    unav_label = "Unavailable"
    if len(availabilities['available'])>0:
        avs = ""
        for av in availabilities['available']:
            avs+="\n - "
            avs+=av
    else:
        avs = "There's nobody available for the moment"

    if len(availabilities['unavailable'])>0:
        unavs = ""
        for unav in availabilities['unavailable']:
            unavs+="\n - "
            unavs+=unav
    else:
        unavs = "There's nobody unavailable for the moment"


    embed = discord.Embed(title="Availabilities", color=0x81455b)
    embed.set_author(name="Roqueboule", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
    embed.add_field(name=av_label, value=avs, inline=False)
    embed.add_field(name=unav_label, value=unavs, inline=False)
    await ctx.send(embed=embed)


        


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)