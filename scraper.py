import requests, json, datetime, TOKENS

url = TOKENS.URL

with open("./data/students.json") as students:
    students = json.load(students)['students']

current_datetime = str(datetime.datetime.now())[:10]
current_datetime = current_datetime.replace("-", "")

# TODO: remove this date for production
current_datetime = "20220207"

url = url.replace("YYYYMMDD", current_datetime)

ids = [n['id'] for n in students]
names = [n['name'] for n in students]

clean = []

for (id, name) in zip(ids, names):
    url_buffer = url.replace('IIII', str(id))
    lessons = json.loads(requests.get(url_buffer).content.decode('utf-8').replace("'", '"'))
    clean_buffer, dict_buffer = [], {}
    print("=====\n"+str(name)+"\n=====")
    dict_buffer['id'] = id
    dict_buffer['name'] = name
    if len(lessons)>0:
        for lesson in lessons:
            print(str(lesson)+"\n")
            # clear keys
            lesson.pop('Description')
            lesson.pop('IdOp')
            lesson.pop('LesGroupes')
            lesson.pop('LibelleLong')
            lesson.pop('SaisieAbsence')
            clean_buffer.append(lesson)
            dict_buffer['agenda'] = clean_buffer
    else:
        dict_buffer['agenda'] = []
        print("> Empty")
    clean.append(dict_buffer)

to_store = {
    "agendas": clean
}

with open("./data/agendas.json", 'w') as outfile:
    json.dump(to_store, outfile, indent=2)
