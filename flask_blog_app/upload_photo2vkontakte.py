import requests
import os
import json
from dotenv import load_dotenv
load_dotenv('vkontakte_ctl/vk.env')

token = os.getenv('VK_USER_TOKEN')
owner_id = os.getenv('VK_OWNER_USER_ID')
album_id = os.getenv('VK_ALBUM_ID_USER')

def get_server_url_for_upload():
    response = requests.post('https://api.vk.com/method/photos.getUploadServer', 
                params={
                    'access_token': token,
                    'v':"5.131",
                    'album_id': album_id,
                    #'group_id': group_id # Идентификатор сообщества, которому принадлежит альбом.
                    }).json()
    upload_url = response['response']['upload_url']
    #print(upload_url)
    return upload_url

def upload_photo2server(url, photo):
    with open(photo, 'rb') as ph:
        files = {'photo': ph}
        response = requests.post(url, files=files)
    response_data = json.loads(response.text)
    server = response_data ['server']
    photos_list = response_data["photos_list"]
    hash = response_data["hash"]
    #print(response.text)
    return server, photos_list, hash

def save_photo2album(server, photos_list, hash):
    response = requests.post('https://api.vk.com/method/photos.save', 
                params={
                    'access_token': token,
                    'v':"5.131",
                    'album_id': album_id,
                    'server': server,
                    'photos_list': photos_list,
                    'hash': hash,
                    }).json()    
    # print(json.dumps(response))
    media_id = response['response'][0]['id']
    #print(media_id)
    return media_id

def add_photo2album(photo):
    url = get_server_url_for_upload()
    server, photos_list, hash = upload_photo2server(url, photo)
    media_id = save_photo2album(server, photos_list, hash)
    return media_id

if __name__ == "__main__":
    photo = 'vkontakte_ctl/my-image.jpeg'
    print(add_photo2album(photo))