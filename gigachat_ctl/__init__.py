import os
import requests
from gigachat import GigaChat
from dotenv import load_dotenv
import logging
from logs import logger as base_logger

load_dotenv('flask_blog_app/.env')

logger = logging.getLogger(__name__)
logger.handlers = base_logger.handlers
logger.setLevel(base_logger.level)

logger.info("Логгер в gigachat_ctl инициирован.")


TOKEN = os.getenv('SBER_GIGACHAT')

def create_text_by_text(question_phrase):
    with GigaChat(credentials=TOKEN, verify_ssl_certs=True) as giga:
        response = giga.chat(question_phrase) # giga chat отдаёт ещё и изображение?
        response_text = response.choices[0].message.content
        result = response_text.split('<')[0]
        logger.info(f"gigachat response :: {response}")
        return result


if __name__ == '__main__':
    question_phrase = 'Опиши в стиле Пушкина Ясное летнее небо утром'
    print(create_text_by_text(question_phrase))