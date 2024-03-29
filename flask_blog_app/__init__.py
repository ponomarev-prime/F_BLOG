import os
import uuid
import time
import logging
from logs import logger as base_logger
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import telegram_ctl as a2tgm
import telegraph_ctl as a2tph
import vkontakte_ctl as a2vk
from db_utils import insert_post, update_post, delete_post, get_post, get_all_posts
from flask import send_from_directory
import gigachat_ctl as neuro_text
import fusionbrain_ai_ctl as neuro_image

from dotenv import load_dotenv
load_dotenv('flask_blog_app/.env')

logger = logging.getLogger(__name__)
logger.handlers = base_logger.handlers
logger.setLevel(base_logger.level)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')

# Log startup information
logger.info("Flask application starting...")
logger.info(f"Debug mode: {app.debug}")
logger.info(f"Running on: {app.config['SERVER_NAME']}")

if app.debug:
    logger.info("Debug mode is enabled. Do not use in production!")

UPLOAD_FOLDER = 'flask_blog_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEFAULT_IMAGE_PATH = 'images/default.jpeg'

current_script_directory = os.path.dirname(os.path.abspath(__file__))

def get_neuro_image(promt):
    post_id = generate_post_id()
    logger.info(f"post_id :: {post_id}")

    # Получаем путь к директории загрузки из конфигурации приложения
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(post_id))
    logger.info(f"upload_folder :: {upload_folder}")
    os.makedirs(upload_folder, exist_ok=True)

    filename = "neuro_img.jpeg"
    filepath = os.path.join(upload_folder, filename)
    logger.info(f"filepath :: {filepath}")

    # Предположим, что у вас есть функция save_img в объекте neuro_image
    path = neuro_image.save_img(filepath, promt)
    logger.info(path)

    # Очищаем путь
    cleaned_path = path.lstrip('/').replace('flask_blog_app/', '')
    logger.info(cleaned_path)

    return cleaned_path

def get_neuro_text(promt):
    result = neuro_text.create_text_by_text(promt)
    return result

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
    logger.info("Попытка отправки в Telegram")
    try:
        tgm_link = a2tgm.sentArt2Channel(f"{title}\n{content}", full_img_path)
        return tgm_link
    except Exception as e:
        logger.error(f"Ошибка при отправке в Telegram: {e}")
        flash(f"Error sending to Telegram: {e}")
        return None

def send_to_tph_link(title, content, full_img_path):
    try:
        logger.info("Попытка отправки в Telegraph")
        tph_link = a2tph.send_art2telegraph(title, content, full_img_path)
        return tph_link
    except Exception as e:
        logger.error(f"Ошибка при отправке в Telegraph: {e}")
        flash(f"Error sending to Telegraph: {e}")
        return None

def send_to_vk_link(title, content, full_img_path):
    try:
        logger.info("Попытка отправки в VKontakte")
        vk_link = a2vk.send_art2vkontakte(f"{title}\n{content}", full_img_path)
        return vk_link
    except Exception as e:
        logger.error(f"Ошибка при отправке в VKontakte: {e}")
        flash(f"Error sending to VKontakte: {e}")
        return None

def send_to_database(title, content, image_path, tgm_link, tph_link, vk_link):
    try:
        logger.info("Попытка отправки в базу данных")
        site_content = f'{content}<br><a href="{tgm_link}">{tgm_link}</a><br><a href="{tph_link}">{tph_link}</a><br><a href="{vk_link}">{vk_link}</a>'           
        insert_post(title, site_content, image_path)
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке в базу данных: {e}")
        flash(f"Error sending to Database: {e}")
        return None

@app.route('/clear_session', methods=['GET'])
def clear_session():
    # Очищаем сессию
    session.clear()

    # Создаем пустую ответную куку с истекшим сроком действия
    response = make_response(redirect(url_for('index')))
    response.set_cookie('session', '', expires=0)
    logger.info("Session is clear...")
    return response

@app.route('/')
def index():
    try:
        logger.info("Запрос к странице index")
        posts = get_all_posts()
        return render_template('index.html', posts=posts, default_image_path=DEFAULT_IMAGE_PATH)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса к странице index: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')  # Перенаправьте пользователя на страницу ошибки или сделайте другую обработку ошибки

@app.route('/<int:post_id>')
def post(post_id):
    try:
        logger.info(f"Запрос к странице post с post_id={post_id}")
        post = get_post(post_id)
        if post and not post.get('image_path'):
            post['image_path'] = 'images/default.jpeg'
        return render_template('post.html', post=post)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса к странице post: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')  # Перенаправьте пользователя на страницу ошибки или сделайте другую обработку ошибки

@app.route('/create', methods=('GET', 'POST'))
def create():
    try:
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
            else:
                image_path = ''

            if chKey and chTitle:
                full_img_path = f'{current_script_directory}/static/{image_path}'
                
                tgm_link = send_to_tgm_link(title, content, full_img_path)
                tph_link = send_to_tph_link(title, content, full_img_path)
                vk_link = send_to_vk_link(title, content, full_img_path)

                send_to_database(title, content, image_path, tgm_link, tph_link, vk_link)
                return redirect(url_for('index'))
            else:
                flash("Something wrong!")
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса create: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')  # Перенаправьте пользователя на страницу ошибки или сделайте другую обработку ошибки
    return render_template('create.html')

@app.route('/create_neuro', methods=('GET', 'POST'))
def create_neuro():
    try:
        if 'post_generated' not in session:
            session['post_generated'] = False
        if 'post_title' not in session:
            session['post_title'] = ''
        if 'post_text' not in session:
            session['post_text'] = ''
        if 'post_image' not in session:
            session['post_image'] = ''
        if 'prepare_button_clicked' not in session:
            session['prepare_button_clicked'] = False
        if 'send_button_clicked' not in session:
            session['send_button_clicked'] = False

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'prepare' and not session['prepare_button_clicked']:
                session['prepare_button_clicked'] = True

                session['post_title'] = request.form['title']
                session['post_text'] = get_neuro_text(request.form['content_promt'])
                logger.info(f"txt :: {session['post_text']}")

                try:
                    session['post_image'] = get_neuro_image(request.form['content_image'])
                except TypeError as e:
                    session['post_image'] = DEFAULT_IMAGE_PATH
                    logger.error(f"Не удалось сгенерировать изображение: {e}")
                    flash('Не удалось сгенерировать изображение!')

                passkey = request.form['passkey']
                createkey = os.getenv('SITE_PASSKEY')

                if passkey != createkey:
                    flash('Key is wrong!')
                elif not session['post_title']:
                    flash('Title is required!')
                else:
                    logger.info(f"title = {session['post_title']},\ncontent_promt = {session['post_text']},\ncontent_image = {session['post_image']},\npasskey = {passkey}")
                    session['post_generated'] = True
            elif action == 'send' and not session['send_button_clicked']:
                session['send_button_clicked'] = True

                full_img_path = f"{current_script_directory}/{session['post_image']}"
                logger.info(f"full_img_path :: {full_img_path}")

                tgm_link = send_to_tgm_link(session['post_title'], session['post_text'], full_img_path)
                tph_link = send_to_tph_link(session['post_title'], session['post_text'], full_img_path)
                vk_link = send_to_vk_link(session['post_title'], session['post_text'], full_img_path)

                logger.info(f"post_image :: {session['post_image']}")
                cleaned_image_path = session['post_image'].lstrip('/').replace('static/', '')
                
                logger.info(f"cleaned_image_path :: {cleaned_image_path}")
                send_to_database(session['post_title'], session['post_text'], cleaned_image_path, tgm_link, tph_link, vk_link)
                
                # Сброс сессии после успешной отправки
                session.clear()

                return redirect(url_for('index'))

        return render_template('create_neuro.html', post_generated=session['post_generated'], post_title=session['post_title'], post_text=session['post_text'], post_image=session['post_image'], prepare_button_clicked=session['prepare_button_clicked'], send_button_clicked=session['send_button_clicked'])
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса create_neuro: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')  # Перенаправьте пользователя на страницу ошибки или сделайте другую обработку ошибки

@app.route('/create_consolidated', methods=('GET', 'POST'))
def create_consolidated():
    return render_template('under_construction.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    try:
        post = get_post(id)

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('Title is required!')
            else:
                update_post(id, title, content)
                logger.info(f"Post with id {id} was successfully updated.")
                return redirect(url_for('index'))

        return render_template('edit.html', post=post)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса edit: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    try:
        post = get_post(id)
        delete_post(id)
        
        logger.info(f"Post with id {id} ('{post['title']}') was successfully deleted.")
        
        flash(f'"{post["title"]}" was successfully deleted!')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Ошибка при удалении поста с id {id}: {e}")
        flash(f"Error deleting post: {e}")
        return render_template('error.html')

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса about: {e}")
        flash(f"Error processing request: {e}")
        return render_template('error.html')