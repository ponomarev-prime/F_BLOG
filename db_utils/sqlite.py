from .config import sqlite_config
import sqlite3


def get_db_connection():
    return sqlite3.connect(sqlite_config['database'])

def insert_post(title, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'INSERT INTO posts (title, content) VALUES (?, ?)'
    cursor.execute(query, (title, content))

    conn.commit()
    cursor.close()
    conn.close()

def update_post(id, title, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'UPDATE posts SET title = ?, content = ? WHERE id = ?'
    cursor.execute(query, (title, content, id))

    conn.commit()
    cursor.close()
    conn.close()

def delete_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'DELETE FROM posts WHERE id = ?'
    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_post(id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Используем row_factory для получения результатов запросов в виде словаря
    cursor = conn.cursor()

    query = 'SELECT * FROM posts WHERE id = ?'
    cursor.execute(query, (id,))
    
    post = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return post

def get_all_posts():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Используем row_factory для получения результатов запросов в виде словаря
    cursor = conn.cursor()

    query = 'SELECT * FROM posts'
    cursor.execute(query)

    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts
