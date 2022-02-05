import requests, os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

response = requests.get(url)

fi = open("./data/agenda.xml", "w")
fi.write(str(response.content))
fi.close()

print("> ok")