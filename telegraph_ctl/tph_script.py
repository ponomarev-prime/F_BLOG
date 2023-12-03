import os
import json
import requests
from html import escape
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv('telegraph_ctl/tph.env')


def read_html(file_path):
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

# Пример использования
html_path='/home/xxx/myscr/F_BLOG/_SENT_DATA_TEST/test_git_parable.html'

article_html = read_html(html_path) #"<div id='article'><p>Hello, world!</p></div>"



article_soup = BeautifulSoup(article_html, features='html.parser')

title = article_soup.find("title").text
content = domToNode(article_soup.find('div')).get('children', [])

api_url = 'https://api.telegra.ph/createPage'
access_token = os.getenv('TPH_TOKEN')

response = requests.post(api_url, json={
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

#print(str(article_soup))
print("---")
# print(data)
print("---")
url = data['result']['url']
print(url)