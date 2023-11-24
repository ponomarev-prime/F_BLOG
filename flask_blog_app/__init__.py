import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import text2telegram as t2t
import os
from dotenv import load_dotenv
load_dotenv()

db_config = {
    'host': os.getenv('BEGET_MYSQL_SERVER'),
    'user': os.getenv('BEGET_MYSQL_USER'),
    'password': os.getenv('BEGET_MYSQL_PASS'),
    'database': os.getenv('BEGET_MYSQL_DB')
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    conn.row_factory = mysql.connector.cursor.MySQLCursorDict
    return conn

def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = 'SELECT * FROM posts WHERE id = %s'
    cursor.execute(query, (post_id,))
    
    post = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if post is None:
        abort(404)

    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = 'SELECT * FROM posts'
    cursor.execute(query)

    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    content = post['content']
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            chTitle=False
        else:
            chTitle=True
        
        if chKey == True and chTitle==True:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = 'INSERT INTO posts (title, content) VALUES (%s, %s)'
            cursor.execute(query, (title, content))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            flash("Somthing wrong!")
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = 'UPDATE posts SET title = %s, content = %s WHERE id = %s'
            cursor.execute(query, (title, content, id))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'DELETE FROM posts WHERE id = %s'
    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))