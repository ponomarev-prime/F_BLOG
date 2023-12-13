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
    image_url = urljoin(source_url, soup.find('img')['src'])
    text = soup.find('article').get_text()
    title = soup.title.text

    # Создаем поддиректорию "img"
    script_directory = os.path.dirname(os.path.realpath(__file__))
    img_directory = os.path.join(script_directory, 'img')
    os.makedirs(img_directory, exist_ok=True)

    # Сохраняем изображение в поддиректорию "img"
    img_file_path = os.path.join(img_directory, 'image.jpg')
    img_data = requests.get(image_url).content
    with open(img_file_path, 'wb') as img_file:
        img_file.write(img_data)

    # Создаем новую HTML-страницу с сохранением форматирования
    new_html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <!-- Вставьте сюда необходимые мета-теги, стили и скрипты -->
        <title>{title}</title>
      </head>
      <body>
        <h1>{title}</h1>
        <p>Автор: <a href="{author_link}" target="_blank">{author_name}</a></p>
        <img src="img/image.jpg" alt="Изображение">
        <p>{text}</p>
        <p>Оригинальная ссылка: <a href="{link}" target="_blank">{link}</a></p>
        <!-- Вставьте сюда необходимые элементы страницы -->
      </body>
    </html>
    """

    # Сохраняем новую HTML-страницу в файл в текущей директории
    file_path = os.path.join(script_directory, 'новая_страница.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_html)

    print(f'HTML-файл сохранен в: {file_path}')
    print(f'Изображение сохранено в: {img_file_path}')

# Пример использования
source_url = 'https://telegra.ph/Post-from-BEGET-12-03-2'
create_html_page(source_url)
