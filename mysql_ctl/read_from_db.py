# pip install mysql-connector-python
import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv(dotenv_path='./flask_blog_app/.env')

# Замените параметры подключения на ваши
db_config = {
    'host': os.getenv('BEGET_MYSQL_SERVER'),
    'user': os.getenv('BEGET_MYSQL_USER'),
    'password': os.getenv('BEGET_MYSQL_PASS'),
    'database': os.getenv('BEGET_MYSQL_DB')
}

# Подключение к базе данных
connection = mysql.connector.connect(**db_config)

try:
    # Создание объекта cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    # SQL-запрос для выборки данных из таблицы (замените на свой запрос)
    query = "SELECT * FROM posts"
    
    # Выполнение запроса
    cursor.execute(query)

    # Получение результатов
    result = cursor.fetchall()

    # Вывод результатов в терминал
    for row in result:
        print(row)

finally:
    # Закрытие курсора и соединения с базой данных
    cursor.close()
    connection.close()
