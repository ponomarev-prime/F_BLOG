import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('vkontakte_ctl/vk.env.env')
from upload_photo2vkontakte import add_photo2album as ph2a

token = os.getenv('VK_USER_TOKEN')
owner_id = os.getenv('VK_OWNER_USER_ID')
owner_id_group = os.getenv('VK_OWNER_IG_GROUP')


msg = 'NEXT'
photo = 'vkontakte_ctl/my-image.jpeg'

type_att = 'photo'
media_id = ph2a(photo)
attachments = f'{type_att}{owner_id}_{media_id}'
attachments = ''

response = requests.post('https://api.vk.com/method/wall.post', 
            params={
                'access_token': token,
                'owner_id': owner_id_group, 
                'from_group': 1,
                'message': msg,
                'signed': 0, 
                'v':"5.131",
                'attachments': attachments
                }).json()
print(json.dumps(response))