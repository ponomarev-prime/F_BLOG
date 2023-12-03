import sqlite3
import os

current_script_directory = os.path.dirname(os.path.abspath(__file__))
#sqlite_db_path = os.path.join(current_script_directory, 'sqlite_database.db')
sqlite_db_path = 'flask_blog_app/db_utils/sqlite_database.db'

def update_sqlite_table():
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    try:
        # PRAGMA foreign_keys = off;
        cursor.execute("PRAGMA foreign_keys = off;")
        
        # BEGIN TRANSACTION;
        cursor.execute("BEGIN TRANSACTION;")

        # Создание временной таблицы
        cursor.execute("CREATE TABLE posts_temp AS SELECT * FROM posts;")

        # Удаление текущей таблицы
        cursor.execute("DROP TABLE posts;")

        # Создание новой таблицы с обновленной структурой
        cursor.execute("""
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                content TEXT NOT NULL,
                created DATETIME DEFAULT CURRENT_TIMESTAMP,
                image_path VARCHAR(255)
            );
        """)

        # Перенос данных из временной таблицы в новую
        cursor.execute("""
            INSERT INTO posts (id, title, content, created, image_path)
            SELECT id, title, content, created, image_path FROM posts_temp;
        """)

        # Удаление временной таблицы
        cursor.execute("DROP TABLE posts_temp;")

        # COMMIT;
        cursor.execute("COMMIT;")

        # PRAGMA foreign_keys = on;
        cursor.execute("PRAGMA foreign_keys = on;")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error updating SQLite table: {e}")
    finally:
        cursor.close()
        conn.close()

update_sqlite_table()
