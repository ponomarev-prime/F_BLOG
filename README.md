![](.gitcontent/f_blog_title.png)
# F BLOG

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


# NEXT 2023-11-21

## App run
```
$ export PYTHONPATH=/home/[xxxx]/[yyyy]]/F_BLOG/flask_blog_app
$ flask --app flask_blog_app run
```

## Add func for sent post to telegram
```
flask_blog_app/text2telegram.py
```
Не забудь про секреты:
```
flask_blog_app/.env

TOKEN=
ID_IT_SPECIAL_FORCES_GROUP=
ID_IT_SPECIAL_FORCES_THREAD=
PASSKEY=
```
