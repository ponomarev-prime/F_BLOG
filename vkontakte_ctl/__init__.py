import requests
import os
import json
from dotenv import load_dotenv
from vkontakte_ctl.upload_photo2vkontakte import add_photo2album as ph2a
import logging

# Загрузка переменных окружения
load_dotenv('flask_blog_app/.env')

# Получение текущей директории скрипта
script_directory = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_directory, 'vkontakte_ctl_log.log')

# Настройка логирования
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Token, user, group
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
    try:
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
        logging.info(f"Text message posted successfully. Post link: {post_link}")
        return post_link
    except Exception as e:
        logging.error(f"Error posting text message: {e}")
        raise

def send_art2vkontakte(msg, image):
    try:
        media_id = ph2a(image)
        type_att = 'photo'
        attachments = create_attachments(type_att, owner_id, media_id)

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
        logging.info(f"Message posted successfully. Post link: {post_link}")
        return post_link
    except Exception as e:
        logging.error(f"Error posting message: {e}")
        raise


if __name__ == "__main__":
    text = "Sent from PYTHON"
    print(send_text2vkontakte(text))

    image = 'gen_img.jpg'
    image_file = os.path.join(script_directory, image)
    #print(send_art2vkontakte(text, image_file))
