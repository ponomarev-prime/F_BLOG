import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('vkontakte_ctl/vk.env')

token = os.getenv('VK_USER_TOKEN')
owner_id = os.getenv('VK_OWNER_USER_ID')
album_id = os.getenv('VK_ALBUM_ID_USER')

response = requests.post('https://api.vk.com/method/photos.get', 
            params={
                'access_token': token,
                'owner_id': owner_id, 
                'v':"5.131",
                'album_id': album_id
                }).json()
print(json.dumps(response))