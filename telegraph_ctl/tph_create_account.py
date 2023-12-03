import os
import json

from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='xxx', author_name='ALEX', author_url='https://t.me/xxx', replace_token=True) # Создаст новый аккаунт

print(telegraph.get_access_token()) # Выведет токен аккаунта
print(json.dumps(telegraph.get_account_info())) # Выведет инфу об аккаунте