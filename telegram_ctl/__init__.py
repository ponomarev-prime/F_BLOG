import requests
import os
import json
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения
load_dotenv('flask_blog_app/.env')

# Получение текущей директории скрипта
script_directory = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_directory, 'telegram_ctl_log.log')

# Настройка логирования
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


TOKEN = os.getenv('TG_TOKEN')
chat_id = os.getenv('ID_DIGITAL_SPIRIT_CHANNEL')
#message_thread_id = os.getenv('ID_IT_SPECIAL_FORCES_THREAD')


def sendText2Channel(data):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

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

    try:
        response_data = response_photo.json()

        if 'result' in response_data:
            # Извлечение данных
            username = response_data['result']['chat']['username']
            message_id = response_data['result']['message_id']
            # Формирование URL
            message_url = f'https://t.me/{username}/{message_id}'
            # Логирование запроса и ответа
            logging.info(f'sentArt2Channel - Request: {json.dumps(payload)}, Response: {response_photo.text}')
        elif 'ok' in response_data and response_data['ok'] is False and response_data['description'] == "Unauthorized":
            # Логирование запроса и ответа
            logging.error(f'sentArt2Channel - Unauthorized, Request: {json.dumps(payload)}, Response: {response_photo.text}')
            # Обработка ошибки Unauthorized
            message_url = None
            print("Error: Unauthorized")
            # Дополнительные действия по обработке ошибки, если необходимо
        else:
            # Логирование запроса и ответа
            logging.error(f'sentArt2Channel - Request: {json.dumps(payload)}, Response: {response_photo.text}')
            # Обработка других случаев, если ключи 'result' или 'url' не найдены
            message_url = None  # или другое значение по умолчанию
            print("Unexpected structure in data")

    except json.JSONDecodeError:
        # Логирование ошибки парсинга JSON
        logging.error(f'sentArt2Channel - JSONDecodeError: {response_photo.text}')
        message_url = None
        print("Error decoding JSON response")
    
    return message_url


if __name__ == "__main__":
    image = 'gen_img.jpg'
    image_file = os.path.join(script_directory, image)

    data = "some text3!"
    
    #print(sendText2Channel(data))
    print(sentArt2Channel(data, image_file))