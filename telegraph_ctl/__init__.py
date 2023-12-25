import os
import json
import requests
from html import escape
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv('flask_blog_app/.env')
from telegraph import Telegraph


def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content

def domToNode(domNode):
    if domNode.name is None:  # Text node
        return domNode.string
    if not domNode.name:  # Non-element node
        return False
    
    nodeElement = {'tag': domNode.name.lower()}
    for attr in domNode.attrs:
        if attr == 'href' or attr == 'src':
            if 'attrs' not in nodeElement:
                nodeElement['attrs'] = {}
            nodeElement['attrs'][attr] = domNode[attr]

    if domNode.contents:
        nodeElement['children'] = [domToNode(child) for child in domNode.contents]

    return nodeElement

def nodeToDom(node):
    if isinstance(node, str):
        return escape(node)

    if 'tag' in node:
        domNode = BeautifulSoup(features='html.parser').new_tag(node['tag'])
        if 'attrs' in node:
            for name, value in node['attrs'].items():
                domNode[name] = value
    else:
        domNode = BeautifulSoup(features='html.parser').new_tag('fragment')

    if 'children' in node:
        for child in node['children']:
            domNode.append(nodeToDom(child))

    return domNode

def send_html2telegraph(html_path):
    article_html = read_html_file(html_path) # читаем html файл
    article_soup = BeautifulSoup(article_html, features='html.parser') # собираем суп

    title = article_soup.find("title").text # забираем Тайтл из html
    content = domToNode(article_soup.find('div')).get('children', []) # собираем контент

    api_url = 'https://api.telegra.ph/createPage'
    access_token = os.getenv('TPH_TOKEN')

    response = requests.post(api_url, json={ # запрос к telegraph api
        'access_token': access_token,
        'title': title,
        'content': json.dumps(content),
        'return_content': True,
        'author_name': 'ALEX',
        'author_url': 'https://t.me/AXV15'
    })

    data = response.json()
    if 'content' in data:
        article_soup.find('div').clear()
        article_soup.find('div').append(nodeToDom({'children': data['content']}))

    if 'result' in data and 'url' in data['result']:
        art_url = data['result']['url']
    elif 'ok' in data and 'error' in data and data['ok'] is False and data['error'] == 'ACCESS_TOKEN_INVALID':
        # Обработка ошибки ACCESS_TOKEN_INVALID
        art_url = None
        print("Error: ACCESS_TOKEN_INVALID")
        # Дополнительные действия по обработке ошибки, если необходимо
    else:
        # Обработка других случаев, если ключи 'result' или 'url' не найдены
        art_url = None  # или другое значение по умолчанию
        print("Unexpected structure in data")
    
    return art_url

def send_text2telegraph(title, text):
    api_url = 'https://api.telegra.ph/createPage'
    access_token = os.getenv('TPH_TOKEN')

    response = requests.post(api_url, json={  # запрос к telegraph api
        'access_token': access_token,
        'title': title,
        'content': [{'tag': 'p', 'children': [text]}],
        'return_content': True,
        'author_name': 'ALEX',
        'author_url': 'https://t.me/AXV15'
    })

    data = response.json()
    if 'content' in data:
        # Можно сделать что-то с контентом, если это нужно
        pass

    art_url = data['result']['url']
    return art_url

def send_art2telegraph(title, text, image_path):
    access_token = os.getenv('TPH_TOKEN')
    telegraph = Telegraph(access_token=access_token)

    src = telegraph.upload_file(image_path)
    src_value = src[0]['src']

    # Создание статьи
    article = telegraph.create_page(
        title=title,
        content=[
            {'tag': 'figure', 'children': [{'tag': 'img', 'attrs': {'src': src_value}}]},
            {'tag': 'p', 'children': [text]}  # Замените текстом вашей статьи
        ],
        author_name = 'ALEX',
        author_url = 'https://t.me/AXV15'
    )

    # Получение ссылки на созданную статью
    article_url = 'https://telegra.ph/{}'.format(article['path'])
    print(article_url)
    return article_url 


if __name__ == "__main__":
    # Пример использования send_html2telegraph
    # html
    relative_path = '_SENT_DATA_TEST/test_git_parable.html'
    # Получаем текущую директорию, из которой выполняется скрипт
    current_directory = os.path.abspath(os.path.dirname(__file__))
    # Поднимаемся на два уровня выше текущей директории
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    #html_path = f'{parent_directory}/{relative_path}'
    #print(html_path)
    #print(send_html2telegraph(html_path))

    # Пример использования send_text2telegraph
    title = 'Title of Text'
    text = 'Hello, world! This is a test text.'
    print(send_text2telegraph(title, text))