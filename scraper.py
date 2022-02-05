import requests, os, json, datetime
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

with open("./data/students.json") as students:
    students = json.load(students)['students']
current_datetime = str(datetime.datetime.now())[:10]
current_datetime = current_datetime.replace("-", "")

# TODO: remove this date for production
# current_datetime = "20220207"

url = url.replace("YYYYMMDD", current_datetime)

ids = [n['id'] for n in students]
ids_str = [str(n['id']) for n in students]
print(ids_str)
names = [n['name'] for n in students]

clean = []

for (id, name) in zip(ids, names):
    url_buffer = url.replace("IIII", str(id))

    # get agenda for current student id
    content = requests.get(url_buffer).content
    if content!=[]:
        content_json = content.decode('utf-8').replace("'", '"')
        agenda = content_json.strip('][').split(', ')
        agenda = agenda[0]
        agenda = agenda.split("}")
        clean_buffer = []
        for ag in agenda:
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
                clean_buffer.append(buffer)
                dict_buffer = {}
                dict_buffer['id'] = id
                dict_buffer['name'] = name
                dict_buffer['agenda'] = clean_buffer
            print(dict_buffer)
            clean.append(dict_buffer)
    else:
        print("> Empty")


to_store = {
    "agendas": clean
}

with open("./data/agendas.json", 'w') as outfile:
    json.dump(to_store, outfile, indent=2)
