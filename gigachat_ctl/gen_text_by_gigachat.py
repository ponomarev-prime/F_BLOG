import os
from dotenv import load_dotenv
load_dotenv('gigachat_ctl/gigachat.env')
from gigachat import GigaChat

TOKEN = os.getenv('SBER_GIGACHAT')

def create_text_by_text(question_phrase):
    with GigaChat(credentials=TOKEN, verify_ssl_certs=True) as giga:
        response = giga.chat(question_phrase)
        return response.choices[0].message.content


if __name__ == '__main__':
    question_phrase = 'Что делает команда curl -X POST localhost:8092/streaming/consolidated/17008132293 -d {"Action": "subscribe", "Symbols": ["GRP1@grp.rt", "GRP2@grp.rt"], "Tids": ["GRP1", "GRP2"]} -H "Content-Type: application/json"'
    print(create_text_by_text(question_phrase))