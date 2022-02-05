import requests, os, json
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

response = requests.get(url)
content = response.content

json_format = content.decode('utf8').replace("'", '"')

agenda_content = json_format.strip('][').split(', ')
agenda_content = agenda_content[0]
agenda_content = agenda_content.split("}")

clean = []

for ag in agenda_content:
    if len(ag)>0:
        if ag[0]==",":
            ag = ag[1:]
        if ag[-1]!="}":
            ag = ag[:len(ag)]+"}"
        if "false" in ag:
            ag = ag.replace("false", '"false"')
        if "null" in ag:
            ag = ag.replace("null", '"null"')
        buffer = json.loads(ag)
        # clean keys
        buffer.pop('Description')
        buffer.pop('IdOp')
        buffer.pop('LesGroupes')
        buffer.pop('LibelleLong')
        buffer.pop('SaisieAbsence')
        clean.append(buffer)

to_store = {
    "agenda": clean
}

with open("./data/agenda.json", 'w') as outfile:
    json.dump(to_store, outfile)

print(f"> {response.status_code}")