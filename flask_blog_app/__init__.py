import os
import uuid
import time
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import telegram_ctl as a2tgm
import telegraph_ctl as a2tph
import vkontakte_ctl as a2vk
from db_utils import insert_post, update_post, delete_post, get_post, get_all_posts
from flask import send_from_directory
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения
load_dotenv('flask_blog_app/.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')

UPLOAD_FOLDER = 'flask_blog_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEFAULT_IMAGE_PATH = 'images/default.jpeg'

# Получение текущей директории скрипта
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Настройка логирования
log_file = os.path.join(current_script_directory, 'flask_log.log')
# Configure Flask logging
app.logger.setLevel(logging.DEBUG)  # Set log level
handler = logging.FileHandler(log_file)  # Log to a file
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')  # Формат сообщения
handler.setFormatter(formatter)
app.logger.addHandler(handler)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_post_id():
    timestamp = int(time.time())
    uuid_part = str(uuid.uuid4().hex)[:8]
    return f"{timestamp}_{uuid_part}"

def save_image(image):
    post_id = generate_post_id()
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(post_id))
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(image.filename)
    filepath = os.path.join(upload_folder, filename)
    image.save(filepath)

    path = f'images/{post_id}/{filename}'
    return path

def send_to_tgm_link(title, content, full_img_path):
    try:
        if full_img_path:
            tgm_link = a2tgm.sentArt2Channel(f"{title}\n{content}", full_img_path)
        else:
            tgm_link = a2tgm.sendText2Channel(f"{title}\n{content}")

        app.logger.info(f"Sent to Telegram. Title: {title}, Content: {content}, Image Path: {full_img_path}")
        return tgm_link
    except Exception as e:
        app.logger.error(f"Error sending to Telegram: {e}")
        flash(f"Error sending to Telegram: {e}")
        return None

def send_to_tph_link(title, content, full_img_path):
    try:
        if full_img_path:
            tph_link = a2tph.send_art2telegraph(title, content, full_img_path)
        else:
            tph_link = a2tph.send_text2telegraph(title, content)

        app.logger.info(f"Sent to Telegraph. Title: {title}, Content: {content}, Image Path: {full_img_path}")
        return tph_link
    except Exception as e:
        app.logger.error(f"Error sending to Telegraph: {e}")
        flash(f"Error sending to Telegraph: {e}")
        return None

def send_to_vk_link(title, content, full_img_path):
    try:
        if full_img_path:
            vk_link = a2vk.send_art2vkontakte(f"{title}\n{content}", full_img_path)
        else:
            vk_link = a2vk.send_text2vkontakte(f"{title}\n{content}")

        app.logger.info(f"Sent to Vkontakte. Title: {title}, Content: {content}, Image Path: {full_img_path}")
        return vk_link
    except Exception as e:
        app.logger.error(f"Error sending to Vkontakte: {e}")
        flash(f"Error sending to VKontakte: {e}")
        return None

def send_to_database(title, content, image_path, tgm_link, tph_link, vk_link):
    try:
        site_content = f'{content}<br><a href="{tgm_link}">{tgm_link}</a><br><a href="{tph_link}">{tph_link}</a><br><a href="{vk_link}">{vk_link}</a>'           
        insert_post(title, site_content, image_path)
        app.logger.info(f"Sent to database. Title: {title}, Content: {content}, Image Path: {image_path}")
        return True
    except Exception as e:
        app.logger.error(f"Error sending to database: {e}")
        flash(f"Error sending to Database: {e}")
        return None

@app.route('/')
def index():
    try:
        posts = get_all_posts()
        app.logger.info("Successfully retrieved posts for index page.")
        return render_template('index.html', posts=posts, default_image_path=DEFAULT_IMAGE_PATH)
    except Exception as e:
        app.logger.error(f"Error in index(): {e}")
        flash(f"An error occurred: {e}")
        return render_template('error.html')  # Свой шаблон для отображения ошибок

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post and not post.get('image_path'):
        post['image_path'] = 'images/default.jpeg'
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        passkey = request.form['passkey']
        createkey = os.getenv('SITE_PASSKEY')
        # Получаем файл из формы
        image = request.files['image']

        if passkey != createkey:
            flash('Key is wrong!')
            chKey=False
        else:
            chKey=True

        if not title:
            flash('Title is required!')
            chTitle=False
        else:
            chTitle=True

        if image and allowed_file(image.filename):
            image_path = save_image(image)
            full_img_path = f'{current_script_directory}/static/{image_path}'
        else:
            image_path = ''
            full_img_path = ''

        if chKey and chTitle:
            
            
            tgm_link = send_to_tgm_link(title, content, full_img_path)
            tph_link = send_to_tph_link(title, content, full_img_path)
            vk_link = send_to_vk_link(title, content, full_img_path)

            send_to_database(title, content, image_path, tgm_link, tph_link, vk_link)
            return redirect(url_for('index'))
        else:
            flash("Somthing wrong!")
    return render_template('create.html')

@app.route('/create_neuro', methods=('GET', 'POST'))
def create_neuro():
    return render_template('under_construction.html')

@app.route('/create_consolidated', methods=('GET', 'POST'))
def create_consolidated():
    return render_template('under_construction.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            update_post(id, title, content)
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    delete_post(id)
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(error):
    app.logger.exception('An exception occurred during a request.')
    return 'Internal Server Error', 500