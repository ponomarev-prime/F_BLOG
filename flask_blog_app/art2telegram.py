import requests
import os
from dotenv import load_dotenv
load_dotenv()

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
    print(response.text)


if __name__ == "__main__":
    data = "some text3!"
    sendText2Channel(data)