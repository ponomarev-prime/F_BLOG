import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('vkontakte_ctl/vk.env')
from vkontakte_ctl.upload_photo2vkontakte import add_photo2album as ph2a

token = os.getenv('VK_USER_TOKEN')
owner_id = os.getenv('VK_OWNER_USER_ID')
owner_id_group = os.getenv('VK_OWNER_IG_GROUP')

def extract_post_link(response, owner_id_group):
    response_dict = json.loads(json.dumps(response))
    post_id = response_dict['response']['post_id']
    post_link = f"https://vk.com/club{owner_id_group[1:]}?w=wall{owner_id_group}_{post_id}%2Fall"
    return post_link

def create_attachments(type_att, owner_id, media_id):
    if media_id:
        attachments = f'{type_att}{owner_id}_{media_id}'
        return attachments
    else:
        return None

def send_text2vkontakte(msg):
    response = requests.post('https://api.vk.com/method/wall.post', 
                params={
                    'access_token': token,
                    'owner_id': owner_id_group, 
                    'from_group': 1,
                    'message': msg,
                    'signed': 0, 
                    'v':"5.131"
                    }).json()
    post_link = extract_post_link(response, owner_id_group)
    return post_link

def send_art2vkontakte(msg, image):
    media_id = ph2a(image)
    type_att = 'photo'
    attachments =create_attachments(type_att, owner_id, media_id)

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
    post_link = extract_post_link(response, owner_id_group)
    return post_link


if __name__ == "__main__":
    text = "Sent from PYTHON"
    print(send_text2vkontakte(text))

    image = 'flask_blog_app/static/images/default.jpeg'
    #print(send_art2vkontakte(text, image))

    # https://vk.com/club223581354?w=wall-223581354_17%2Fall
    # {"response": {"post_id": 17}}