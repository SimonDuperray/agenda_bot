import json, pprint

with open("./data/agenda.json") as json_outfile:
    lessons = json.load(json_outfile)['agenda']

for lesson in lessons:
    pprint.pprint(lesson)
    print("\n")
