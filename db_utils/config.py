import os
from dotenv import load_dotenv
load_dotenv('flask_blog_app/.env')

current_script_directory = os.path.dirname(os.path.abspath(__file__))

mysql_config = {
    'host': os.getenv('BEGET_MYSQL_SERVER'),
    'user': os.getenv('BEGET_MYSQL_USER'),
    'password': os.getenv('BEGET_MYSQL_PASS'),
    'database': os.getenv('BEGET_MYSQL_DB')
}

sqlite_config = {
    'database': f'{current_script_directory}/sqlite_database.db'
}
