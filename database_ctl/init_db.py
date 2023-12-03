import sqlite3

connection = sqlite3.connect('.flask_blog_app/db_utils/sqlite_database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Database initial post', 'Database initial post, please delete it later.')
            )

connection.commit()
connection.close()