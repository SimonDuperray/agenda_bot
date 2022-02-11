# AgendaBot ESEO

## Getting started

You need to install some python packages with pip:

```
discord: 1.7.3
json: x
datetime: x
requests: 2.26.0
```

You have to create a <i>students.json</i> file in <b>data</b> folder and to fill it with a certain format:

```json
{
    "students": [
        {
            "name": "student_name",
            "id": 00000
        }
    ]
}
```

You also have to create a <i>agendas.json</i> file in <b>data</b> folder. It is in this file that all agendas will be stored. <i>agendas.json</i> must follows the following format:

```json
{
    "agendas": []
}
```

I didn't want that the scraper will send request to the proxy for every Discord command, so I've programmed the execution of the scraper every day at 1:00 am with crontab with the following command:

```python
0 1 * * * sudo /usr/bin/python3 /home/pi/Documents/agenda_bot/scraper.py > /home/pi/Documents/agenda_bot/logs/bot_log.log 2>&1
```

For each Discord command, the script will parse the json file and not send request to the proxy.

The url for the GET request is parameterized, I send the time range and all users's ids to get their agendas.

## Running

Once the bot is created, you only have to send <b>#dispo</b> and the bot will send you an dynamic embedded message according to the current situation. If there is no lesson for the current day, a custom message appears, but if only some students are in class, another message is sent.

## Help

You can contact me for every question you may have.