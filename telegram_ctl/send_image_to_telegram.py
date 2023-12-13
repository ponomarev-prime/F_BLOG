import requests
import os
import json
import sys
from dotenv import load_dotenv
load_dotenv('tgm.env')

TOKEN = os.getenv('TG_TOKEN')
chat_id = os.getenv('ID_IT_SPECIAL_FORCES_GROUP')
message_thread_id = os.getenv('ID_IT_SPECIAL_FORCES_THREAD')

message = "test"

img_path='gen_img.jpeg'
image_caption=message

url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

data = {"chat_id": chat_id, "caption": image_caption, "message_thread_id": message_thread_id}

with open(img_path, "rb") as image_file:
    responseData = requests.post(url, data=data, files={"photo": image_file}).json()

json_string = json.dumps(responseData)
print(json_string)