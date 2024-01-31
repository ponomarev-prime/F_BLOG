import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

# Создайте объект RotatingFileHandler для логирования в файл
log_file = 'logs/flask_blog.log'
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)  # Максимальный размер 1 МБ, хранить 5 бэкапов

# Создайте форматтер и добавьте его к обработчику
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s - %(message)s')
handler.setFormatter(formatter)

# Добавьте обработчик к объекту логгера
logger.addHandler(handler)
logger.setLevel(logging.INFO)