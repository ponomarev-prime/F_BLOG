import os
import json
from dotenv import load_dotenv
load_dotenv()
from telegraph import Telegraph

TOKEN = os.getenv('TPH_TOKEN')
telegraph = Telegraph(access_token=TOKEN)

def send_art2telegraph():
    response = telegraph.create_page(
        title='Test_page',
        html_content='<p>Hello, world!</p>\n Some text X1',
        author_name='ALEX',
        author_url='https://t.me/AXV15',
    )
    print(json.dumps(response)) # Для того чтобы возвращаемый JSON бы валидным и чиатлся | jq .


if __name__ == "__main__":
    #html = f"<p>Hello, world!</p> EEE X1",
    send_art2telegraph()
