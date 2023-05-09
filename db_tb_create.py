# db and table create

import sqlite3
from datetime import datetime

db = 'news.db'

def create_database(db):
    # Создаем базу данных
    conn = sqlite3.connect(db)

    # Создаем таблицу Google_News
    # id, created_at, prefix, title, link
    conn.execute('''CREATE TABLE IF NOT EXISTS Google_News 
                    (id INTEGER PRIMARY KEY NOT NULL, 
                    created_at TEXT NOT NULL, 
                    prefix TEXT, 
                    title TEXT, 
                    link TEXT);''')

    conn.commit()
    conn.close()
    
    return ()

create_database(db)