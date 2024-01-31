import requests
import os
import json
from dotenv import load_dotenv
import logging
from logs import logger as base_logger

load_dotenv('flask_blog_app/.env')

logger = logging.getLogger(__name__)
logger.handlers = base_logger.handlers
logger.setLevel(base_logger.level)

logger.info("Логгер в telegram_ctl инициирован.")

TOKEN = os.getenv('TG_TOKEN')
chat_id = os.getenv('ID_DIGITAL_SPIRIT_CHANNEL')
#message_thread_id = os.getenv('ID_IT_SPECIAL_FORCES_THREAD')
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def sendText2Channel(data):
    payload = {
        "text": data,
        "chat_id": chat_id,
        #"message_thread_id": message_thread_id,
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "parse_mode": "markdown"
    }
    headers = {
        "accept": "application/json",
        "User-Agent": "F_BLOG",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    response_data = json.loads(response.text)

    # Извлечение данных
    username = response_data['result']['chat']['username']
    message_id = response_data['result']['message_id']
    # Формирование URL
    message_url = f'https://t.me/{username}/{message_id}'
    return(message_url)

def sentArt2Channel(data, image_path):
    # Открываем изображение в бинарном режиме
    with open(image_path, "rb") as image_file:
        img = image_file.read()

    # Параметры запроса для отправки фото
    files = {'photo': ('image.jpg', img)}

    # Параметры запроса для отправки текста
    payload = {
        "chat_id": chat_id,
        "caption": data,  # Текст к изображению
        "disable_web_page_preview": False,
        "disable_notification": False,
        "parse_mode": "markdown"
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "F_BLOG"
    }

    # URL для отправки фото
    photo_url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    # Отправка запроса на отправку фото
    response_photo = requests.post(photo_url, headers=headers, params=payload, files=files)

    # Извлечение данных
    response_data = json.loads(response_photo.text)
    username = response_data['result']['chat']['username']
    message_id = response_data['result']['message_id']

    # Формирование URL
    message_url = f'https://t.me/{username}/{message_id}'
    
    logger.info(f"message_url :: {message_url}")
    return message_url


if __name__ == "__main__":
    data = "some text3!"
    image = 'gen_img.jpeg'
    #print(sendText2Channel(data))
    print(sentArt2Channel(data, image))