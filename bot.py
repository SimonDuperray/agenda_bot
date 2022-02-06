import discord, json, os, datetime, TOKENS
from discord.ext import commands
# from dotenv import load_dotenv
from plistlib import load

# load_dotenv()

# DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_TOKEN = TOKENS.DISCORD_TOKEN    

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
    en_cours = []

    with open('./data/agendas.json') as agendas:
        agendas = json.load(agendas)['agendas']
    print(len(agendas))
    if len(agendas)==0:
        en_cours.append("Weekend")
    else:
        now = datetime.datetime.now()
        # now = now.replace(hour=9, minute=0, second=0, microsecond=0, day=7)
        for agenda in agendas:
            print(f"{agenda['name']}'s agenda: ")
            for lesson in agenda['agenda']:
                starth = int(lesson['Debut'][11:13])
                startm = int(lesson['Debut'][14:16])
                starts = int(lesson['Debut'][17:19])
                endh = int(lesson['Fin'][11:13])
                endm = int(lesson['Fin'][14:16])
                ends = int(lesson['Fin'][17:19])

                start=now.replace(hour=starth, minute=startm, second=starts, microsecond=0)
                end=now.replace(hour=endh, minute=endm, second=ends, microsecond=0)

                print(now)
                
                if end>now and start<now:
                    if agenda['name'] not in en_cours:
                        en_cours.append(agenda['name'])

    if en_cours==[]:
        en_cours.append("Personne n'est en cours actuellement")

    if len(en_cours)==1:
        if en_cours[0]=="Weekend":
            print("Weekend")
            name = "Pas cours..."
            value = "Personne a cours aujourd'hui. Va te plutôt te reposer !"
        if en_cours[0]=="Personne n'est en cours actuellement":
            print("personne en cours")
            name = "Ptit baby ?"
            value = "Y a personne en cours, go caffet pour un ptit baby"
    else:
        print("en cours")
        name="Heureusement qu'il y en a qui travaillent"
        value=""
        for student in en_cours:
            value+="\n - "
            value+=student
            


    embed = discord.Embed(title="Availabilities", color=0x81455b)
    embed.set_author(name="Roqueboule", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
    embed.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
