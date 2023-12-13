import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
#url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

responseData = requests.get(url).json()

json_string = json.dumps(responseData)
print(json_string)

#print(requests.Session().headers)
#print(os.getpid())