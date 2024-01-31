# GIGACHAT API

It's simple, just let it lie here.

https://developers.sber.ru/docs/ru/gigachat/overview

https://github.com/ai-forever/gigachat

short flow:
```bash
pip install -r requirements.txt
```
# Не забудь установить серт на хостинге!!!
```bash
curl -k "https://gu-st.ru/content/Other/doc/russian_trusted_root_ca.cer" -w "\n" >> $(python3 -m certifi)
```

`.env`
```
SBER_GIGACHAT=<Авторизационные данные>

GIGACHAT_CREDENTIALS=<Client ID>
GIGACHAT_SCOPE=<Scope>
GIGACHAT_VERIFY_SSL_CERTS=<True|False>
```