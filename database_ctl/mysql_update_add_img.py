import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv('flask_blog_app/.env')

mysql_config = {
    'host': os.getenv('BEGET_MYSQL_SERVER'),
    'user': os.getenv('BEGET_MYSQL_USER'),
    'password': os.getenv('BEGET_MYSQL_PASS'),
    'database': os.getenv('BEGET_MYSQL_DB')
}

def update_mysql_table():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        # ALTER TABLE
        cursor.execute("ALTER TABLE posts ADD COLUMN image_path VARCHAR(255)")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error updating MySQL table: {e}")
    finally:
        cursor.close()
        conn.close()

update_mysql_table()
