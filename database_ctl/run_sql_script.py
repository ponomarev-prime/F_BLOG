import sqlite3
import os

sqlite_db_path = 'flask_blog_app/db_utils/sqlite_database.db'

def execute_sql_script(script):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    try:
        for statement in script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print(f"Error executing SQL script: {e}")
    finally:
        cursor.close()
        conn.close()

# SQL-скрипт
sql_script = """
PRAGMA foreign_keys = off;

-- Создание временной таблицы
CREATE TABLE IF NOT EXISTS posts_temp AS SELECT * FROM posts;

-- Удаление текущей таблицы
DROP TABLE IF EXISTS posts;

-- Создание новой таблицы с обновленной структурой
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    image_path VARCHAR(255)
);

-- Перенос данных из временной таблицы в новую
INSERT INTO posts (id, title, content, created)
SELECT id, title, content, created FROM posts_temp;

-- Удаление временной таблицы
DROP TABLE IF EXISTS posts_temp;

PRAGMA foreign_keys = on;
"""

# Выполнение SQL-скрипта
result = execute_sql_script(sql_script)

# Вывод результата (если нужно)
print(result)