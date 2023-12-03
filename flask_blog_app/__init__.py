import os
import uuid
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import flask_blog_app.art2telegram as a2tgm
import flask_blog_app.art2telegraph_v2 as a2tph
import flask_blog_app.art2vkontakte_v2 as a2vk
from flask_blog_app.db_utils import insert_post, update_post, delete_post, get_post, get_all_posts
from flask import send_from_directory

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')

UPLOAD_FOLDER = 'flask_blog_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEFAULT_IMAGE_PATH = 'images/default.jpeg'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_post_id():
    return str(uuid.uuid4().hex)[:8]

def save_image(image):
    post_id = generate_post_id()
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(post_id))
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(image.filename)
    filepath = os.path.join(upload_folder, filename)
    image.save(filepath)

    path = f'images/{post_id}/{filename}'
    return path

@app.route('/')
def index():
    posts = get_all_posts()
    return render_template('index.html', posts=posts, default_image_path=DEFAULT_IMAGE_PATH)

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
        else:
            image_path = ''

        if chKey == True and chTitle==True:
            insert_post(title, content, image_path)
            print(a2tgm.sendText2Channel(f"{title}\n{content}"))
            print(a2tph.send_text2telegraph(title, content))
            print(a2vk.send_text2vkontakte(f"{title}\n{content}"))
            print(passkey)
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
