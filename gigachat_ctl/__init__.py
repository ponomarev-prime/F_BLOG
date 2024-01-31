import os
import requests
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv('gigachat_ctl/gigachat.env')

TOKEN = os.getenv('SBER_GIGACHAT')

def create_text_by_text(question_phrase):
    with GigaChat(credentials=TOKEN, verify_ssl_certs=True) as giga:
        response = giga.chat(question_phrase) # giga chat отдаёт ещё и изображение?
        response_text = response.choices[0].message.content
        result = response_text.split('\n')[0]
        return result


if __name__ == '__main__':
    question_phrase = 'Опиши в стиле Пушкина Ясное летнее небо утром'
    print(create_text_by_text(question_phrase))