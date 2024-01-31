<img src=".gitcontent/f_blog_title.png" alt="Flask Blog Title" width="1024">


Below is a sample README for Flask blog application:

# Flask Blog Application

This is a simple Flask blog application for publishing articles with images. Users can create, edit, and delete posts. The application also provides integration with Telegram, Telegraph, and VKontakte for sharing posts.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Routes](#routes)

## Features

- Create, edit, and delete blog posts.
- Upload images along with the posts.
- Integration with Telegram, Telegraph, and VKontakte for sharing posts.
- Database storage for posts.

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python
- Flask
- Telegram API key (for Telegram integration)
- Telegraph API key (for Telegraph integration)
- VKontakte API key (for VKontakte integration)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ponomarev-prime/F_BLOG.git
cd F_BLOG
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the root directory with the following content:

```plaintext
FLASK_SECRET=
DB_TYPE=mysql (or sqlite)

BEGET_MYSQL_SERVER=
BEGET_MYSQL_USER=
BEGET_MYSQL_PASS=
BEGET_MYSQL_DB=

TG_TOKEN=
ID_DIGITAL_SPIRIT_CHANNEL=

VK_USER_TOKEN=
VK_OWNER_IG_GROUP=
VK_OWNER_USER_ID=
VK_ALBUM_ID_USER=

TPH_TOKEN=
```

2. Set up your Telegram, Telegraph, and VKontakte API keys in the respective modules (`telegram_ctl.py`, `telegraph_ctl.py`, `vkontakte_ctl.py`).

## Usage

Run the Flask application:

Create `.flaskenv`
```
PYTHONPATH=/home/[path]/F_BLOG/flask_blog_app
FLASK_APP=flask_blog_app
```

Run
```bash
flask run
```

Visit `http://localhost:5000` in your browser to access the application.

## Routes

- `/`: Home page displaying all blog posts.
- `/<int:post_id>`: Display a specific blog post.
- `/create`: Create a new blog post.
- `/create_neuro`: Under construction page for a future feature.
- `/create_consolidated`: Under construction page for another future feature.
- `/<int:id>/edit`: Edit an existing blog post.
- `/<int:id>/delete`: Delete an existing blog post.


# F BLOG [where it all began]

FlaskBlog :: View, Create, Edit, Delete.

```
(.venv) PS C:\Users\ponom\Documents\CODE\F_BLOG\flask_blog_app> flask run
```

1
![](.gitcontent/f_blog1.png)

2
![](.gitcontent/f_blog2.png)

3
![](.gitcontent/f_blog3.png)

# Hosting

It's works from Beget https://beget.com/

https://f-blog.ponomarev-aa.ru/

(2023-05-10)

![](.gitcontent/irinastamislavovna.png)

# cURL :: POST

```
curl -X POST -d "title=Hello from cURL" -d "content=cURL POST запрос" https://f-blog.ponomarev-aa.ru/create
```

![](.gitcontent/curl_post_x.png)


# Tips

### diff

```
(.venv) $ diff <(cat requirements.txt | tr  "\>\=" " ")  <(cat requirements.stable.txt | tr  "\=\=" " ") -y
annotated-types  0.6.0						annotated-types  0.6.0
anyio  4.1.0						      |	anyio  4.2.0
beautifulsoup4  4.12.2					      |	beautifulsoup4  4.12.3
blinker  1.7.0							blinker  1.7.0
certifi  2023.11.17						certifi  2023.11.17
charset-normalizer  3.3.2					charset-normalizer  3.3.2
click  8.1.7							click  8.1.7
colorama  0.4.6							colorama  0.4.6
exceptiongroup  1.2.0						exceptiongroup  1.2.0
Flask  3.0.0						      |	Flask  3.0.1
gigachat  0.1.8						      |	gigachat  0.1.13
h11  0.14.0							h11  0.14.0
httpcore  1.0.2							httpcore  1.0.2
httpx  0.25.2						      |	httpx  0.26.0
idna  3.4						      |	idna  3.6
itsdangerous  2.1.2						itsdangerous  2.1.2
Jinja2  3.1.2						      |	Jinja2  3.1.3
Markdown  3.5.1						      |	Markdown  3.5.2
MarkupSafe  2.1.3					      |	MarkupSafe  2.1.4
mysql-connector-python  8.2.0				      |	mysql-connector-python  8.3.0
Pillow  10.1.0						      |	pillow  10.2.0
protobuf  4.21.12					      |	protobuf  4.25.2
pydantic  2.5.2						      |	pydantic  2.6.0
pydantic_core  2.14.5					      |	pydantic_core  2.16.1
python-dotenv  1.0.0					      |	python-dotenv  1.0.1
requests  2.31.0						requests  2.31.0
sniffio  1.3.0							sniffio  1.3.0
soupsieve  2.5							soupsieve  2.5
telegraph  2.2.0						telegraph  2.2.0
typing_extensions  4.8.0				      |	typing_extensions  4.9.0
urllib3  2.1.0						      |	urllib3  2.2.0
Werkzeug  3.0.1							Werkzeug  3.0.1
```