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

@bot.command(name="array", help="Test for embedding arrays in message")
async def array(ctx):
    output = t2a(
        header=header,
        body=[
            ["Alexandre", "yes", "NT", "BDDR"], 
            ["Marcelin", "no", "T", "Scrum"], 
        ]
    )
    output = "```\n"+str(output)+"\n```"
    # await ctx.send(f"```\n{output}\n```")

    embed = discord.Embed(title="Availabilities", color=0x81455b)
    embed.set_author(name="ESEO Grande à Angers", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
    embed.add_field(name="eee", value=output, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="dispo", help="Check availability of students")
async def dispo(ctx):
    
    with open("./data/agendas.json") as agendas:
        agendas = json.load(agendas)['agendas']

    state = "weekend" if len(agendas)==0 else "week"

    embed = discord.Embed(title='Availabilites', color=0x81455b)
    embed.set_author(name="ESEO Grande à Angers", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
    

    if state=="weekend":
        name="Weekend"
        value = "c'est le weekend"
    else:
        students_list, isBusy_list, types_list, lessons_list = [], [], [], []
        for student in agendas:
            students_list.append(student['name'].split(" ")[0])
            now = datetime.datetime.now()
            now = now.replace(hour=9, minute=0, second=0, microsecond=0, day=7)
            print(f"> Student: {student['name']}")
            states = []
            for lesson in student['agenda']:
                starth = int(lesson['Debut'][11:13])
                startm = int(lesson['Debut'][14:16])
                starts = int(lesson['Debut'][17:19])
                endh = int(lesson['Fin'][11:13])
                endm = int(lesson['Fin'][14:16])
                ends = int(lesson['Fin'][17:19])

                start=now.replace(hour=starth, minute=startm, second=starts, microsecond=0)
                end=now.replace(hour=endh, minute=endm, second=ends, microsecond=0)

                print(f"   > Lesson: {lesson['Libelle']} - {end>now and start<now}")

                if end>now and start<now:
                    states.append(True)
                else:
                    states.append(False)
                    

            if True in states:
                isBusy_list.append('yes')
                types_list.append("NT" if "non tutorée" in lesson['Libelle'] else "T")
                lessons_list.append(lesson['Libelle'])
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

    embed.add_field(name=name, value=value, inline=False)
    await ctx.send(embed=embed)


# @bot.command(name="dispo", help="Check availability of students")
# async def dispo(ctx):  
#     en_cours = []

#     with open('./data/agendas.json') as agendas:
#         agendas = json.load(agendas)['agendas']
        
#     state = "weekend" if len(agendas)==0 else "week"

#     if state=="weekend":
#         en_cours.append("Weekend")
#     else:
#         now = datetime.datetime.now()
#         now = now.replace(hour=9, minute=0, second=0, microsecond=0, day=7)
#         for agenda in agendas:
#             print(f"{agenda['name']}'s agenda: ")
#             for lesson in agenda['agenda']:
                # starth = int(lesson['Debut'][11:13])
                # startm = int(lesson['Debut'][14:16])
                # starts = int(lesson['Debut'][17:19])
                # endh = int(lesson['Fin'][11:13])
                # endm = int(lesson['Fin'][14:16])
                # ends = int(lesson['Fin'][17:19])

#                 start=now.replace(hour=starth, minute=startm, second=starts, microsecond=0)
#                 end=now.replace(hour=endh, minute=endm, second=ends, microsecond=0)

#                 print(now)
                
#                 if end>now and start<now:
#                     if agenda['name'] not in en_cours:
#                         en_cours.append(agenda['name'])

#     if en_cours==[]:
#         en_cours.append("Personne n'est en cours actuellement")

#     if len(en_cours)==1:
#         if en_cours[0]=="Weekend":
#             print("Weekend")
#             name = "Pas cours..."
#             value = "Personne a cours aujourd'hui. Va te plutôt te reposer !"
#         if en_cours[0]=="Personne n'est en cours actuellement":
#             print("personne en cours")
#             name = "Ptit baby ?"
#             value = "Y a personne en cours, go caffet pour un ptit baby"
#     else:
#         print("en cours")
#         name="Heureusement qu'il y en a qui travaillent"
#         value=""
#         for student in en_cours:
#             value+="\n - "
#             value+=student
            
#     embed = discord.Embed(title="Availabilities", color=0x81455b)
#     embed.set_author(name="ESEO Grande à Angers", icon_url="https://cdn3.iconfinder.com/data/icons/school-174/48/school_bold-12-512.png")
#     embed.add_field(name=name, value=value, inline=False)
#     await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
