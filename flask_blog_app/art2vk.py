import requests
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('VK_TOKEN') # VK_TOKEN str ваш токен #разрешить работу с группой и смс для токена
owner_id_group = os.getenv('VK_OWNER_IG_GROUP')  # VK_OWNER_IG_GROUP  itn-число знак минус для id группы itn-число


msg = 'Good job!'

response = requests.post('https://api.vk.com/method/wall.post', 
            params={
                'access_token': token,
                'owner_id': owner_id_group, 
                'from_group': 1,
                'message': msg,
                'signed': 0, 
                'v':"5.131"
                }).json()
print(response)