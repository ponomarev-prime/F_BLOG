import json
import time
import requests
import os
import io, base64
from PIL import Image
from dotenv import load_dotenv
import logging

load_dotenv('flask_blog_app/.env')

# Инициализация логгера в другом файле
logger = logging.getLogger(__name__)
logger.info("Логгер в fusionbrain_ai_ctl инициирован.")

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

def create_image_by_text(text):
    API_KEY = os.getenv('FUSION_API_KEY')
    SECRET_KEY = os.getenv('FUSION_SECRET_KEY')

    logger.info(f"crt img :: {text}")
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(images[0], "utf-8"))))
    logger.info(f"fff :: {img}")
    return img

def save_img(path, gen_phrase):
    img = create_image_by_text(gen_phrase)
    img.save(path)
    return path

if __name__ == '__main__':
    gen_phrase = "Clear summer sky in the morning"
    output_image_file = 'gen_img.jpeg'
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    path = f"{current_script_directory}/{output_image_file}"
    print(path)
    img = create_image_by_text(gen_phrase)
    img.save(path)
