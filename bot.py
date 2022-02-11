import discord, json, datetime, TOKENS
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle

DISCORD_TOKEN = TOKENS.DISCORD_TOKEN    

intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="#", intents=intents)

header=["Student", "isBusy", "N/NT", "Lesson"]

@bot.event
async def on_ready():
    print("> Bot connected")
    await bot.change_presence(activity=discord.Game(name="#help"))

@bot.command(name="disconnect", help="Disconnect the bot from the server [only admin]")
async def disconnect(ctx):
    if str(ctx.message.author)=="Kartodix#2540":
        await ctx.send("I have to go. Bye!")
        await client.close()
    else:
        await ctx.send("You're not allowed to run this command!")

@bot.command(name="dispo", help="Check availability of students")
async def dispo(ctx):
    
    with open("./data/agendas.json") as agendas:
        agendas = json.load(agendas)['agendas']

    embed = discord.Embed(title='Availabilites', color=0x81455b)
    embed.set_author(name="ESEO Grande à Angers", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
    
    students_list, isBusy_list, types_list, lessons_list = [], [], [], []
    for student in agendas:
        students_list.append(student['name'].split(" ")[0])
        now = datetime.datetime.now()
        # now = now.replace(hour=14, minute=0, second=0, microsecond=0, day=7)
        print(f"> Student: {student['name']}\n{student['agenda']}")
        states, types = [], []
        for lesson in student['agenda']:
            starth = int(lesson['Debut'][11:13])
            startm = int(lesson['Debut'][14:16])
            starts = int(lesson['Debut'][17:19])
            endh = int(lesson['Fin'][11:13])
            endm = int(lesson['Fin'][14:16])
            ends = int(lesson['Fin'][17:19])

            start=now.replace(hour=starth, minute=startm, second=starts, microsecond=0)
            end=now.replace(hour=endh, minute=endm, second=ends, microsecond=0)

            # print(f"   > Lesson: {lesson['Libelle']} - {end>now and start<now} - {'non' in lesson['Libelle']}")

            states.append(True if end>now and start<now else False)
            types.append("NT" if "non" in lesson['Libelle'] else "T")

        if True in states:
            isBusy_list.append('yes')
            # if index of true in states == index of NT in types then NT else T
            if "NT" in types:
                cond = states.index(True)==types.index("NT")
            else:
                cond = False

            types_list.append("NT" if cond else "T")
            lesson = lesson['Libelle']
            lesson = lesson[:int(lesson.find("("))] + lesson[int(lesson.find(")"))+1:]
            lesson = lesson[:int(lesson.find("-"))]
            lesson = lesson[:int(lesson.find(":"))]
            lessons_list.append(lesson)
        else:
            isBusy_list.append('no')
            types_list.append("*")
            lessons_list.append("*")
                
        body=[]
        for (student, isBusy, type, lesson) in zip(students_list, isBusy_list, types_list, lessons_list):
            body.append([
                student, isBusy, type, lesson
            ])

        print(len(students_list), len(isBusy_list), len(types_list), len(lessons_list))

        name="Week"
        value=t2a(
            header=header,
            body=body
        )
        value="```\n"+str(value)+"\n```"

    embed.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
