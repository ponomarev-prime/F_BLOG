import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_html_page(source_url):
    # Загружаем исходную HTML-страницу
    response = requests.get(source_url)
    source_html = response.text

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(source_html, 'html.parser')

    # Извлекаем нужную информацию
    link = soup.find('link', {'rel': 'canonical'})['href']
    author_name = soup.find('a', {'rel': 'author'}).text
    author_link = soup.find('a', {'rel': 'author'})['href']

    # Проверяем наличие тега img
    img_tag = soup.find('img')
    if img_tag:
        image_url = urljoin(source_url, img_tag['src'])
        
        # Создаем поддиректорию "img"
        script_directory = os.path.dirname(os.path.realpath(__file__))
        img_directory = os.path.join(script_directory, 'img')
        os.makedirs(img_directory, exist_ok=True)

        # Сохраняем изображение в поддиректорию "img"
        img_file_path = os.path.join(img_directory, 'image.jpg')
        img_data = requests.get(image_url).content
        with open(img_file_path, 'wb') as img_file:
            img_file.write(img_data)
    else:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        img_file_path = None

    text = soup.find('article').get_text()
    title = soup.title.text

    # Читаем шаблон из файла
    template_file_path = os.path.join(script_directory, 'template.html')
    with open(template_file_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()

    # Подставляем значения в шаблон
    template = template.format(
        title=title,
        author_link=author_link,
        author_name=author_name,
        text=text,
        link=link,
        img_path=img_file_path.replace(script_directory, '').lstrip(os.path.sep) if img_file_path else ''
    )

    # Сохраняем новую HTML-страницу в файл в текущей директории
    file_path = os.path.join(script_directory, 'новая_страница2.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(template)

    print(f'HTML-файл сохранен в: {file_path}')
    if img_file_path:
        print(f'Изображение сохранено в: {img_file_path}')

# Пример использования
source_url = 'https://telegra.ph/The-Git-Parable-12-13-4'  # 'https://telegra.ph/Post-from-BEGET-12-03-2'
create_html_page(source_url)
