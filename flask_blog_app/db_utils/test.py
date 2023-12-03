from .config import mysql_config
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(**mysql_config)

def insert_post(title, content, image_path=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'INSERT INTO posts (title, content, image_path) VALUES (%s, %s, %s)'
    cursor.execute(query, (title, content, image_path))

    conn.commit()
    cursor.close()
    conn.close()


def delete_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'DELETE FROM posts WHERE id = %s'
    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_post(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = 'SELECT * FROM posts WHERE id = %s'
    cursor.execute(query, (id,))
    
    post = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return post

def get_all_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = 'SELECT * FROM posts'
    cursor.execute(query)
    
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return posts
