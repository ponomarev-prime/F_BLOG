import os
from .mysql import insert_post as mysql_insert_post, \
    update_post as mysql_update_post, delete_post as mysql_delete_post, \
    get_post as mysql_get_post, get_all_posts as mysql_get_all_posts
from .sqlite import insert_post as sqlite_insert_post, \
    update_post as sqlite_update_post, delete_post as sqlite_delete_post, \
    get_post as sqlite_get_post, get_all_posts as sqlite_get_all_posts

default_type = 'mysql'  # sqlite, mysql
selected_type = os.getenv('DB_TYPE', default_type)

def insert_post(title, content, image_path):
    if selected_type == 'mysql':
        return mysql_insert_post(title, content, image_path)
    elif selected_type == 'sqlite':
        return sqlite_insert_post(title, content, image_path)
    else:
        raise ValueError('Unsupported database type')

def update_post(id, title, content):
    if selected_type == 'mysql':
        return mysql_update_post(id, title, content)
    elif selected_type == 'sqlite':
        return sqlite_update_post(id, title, content)
    else:
        raise ValueError('Unsupported database type')

def delete_post(id):
    if selected_type == 'mysql':
        return mysql_delete_post(id)
    elif selected_type == 'sqlite':
        return sqlite_delete_post(id)
    else:
        raise ValueError('Unsupported database type')

def get_post(id):
    if selected_type == 'mysql':
        return mysql_get_post(id)
    elif selected_type == 'sqlite':
        return sqlite_get_post(id)
    else:
        raise ValueError('Unsupported database type')

def get_all_posts():
    if selected_type == 'mysql':
        return mysql_get_all_posts()
    elif selected_type == 'sqlite':
        return sqlite_get_all_posts()
    else:
        raise ValueError('Unsupported database type')
