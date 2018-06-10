import requests
import CatOrDog
from urllib.request import urlretrieve

token1 = '531282244:AAF8MJ_Ii7CLLSToSLmdq-QT48t857iFRlI'
URL = 'https://api.telegram.org/bot' + token1 + '/'
URL1 = 'https://api.telegram.org/file/bot' + token1 + '/'
next_photo = 0

def PhotoGet(data):
    chat_id = data['result'][-1]['message']['chat']['id']
    photo_id = data['result'][-1]['message']['photo'][-1]['file_id']
    global next_photo

    if photo_id != next_photo:
        next_photo = photo_id
        photo_url = URL + 'getFile?file_id=' + photo_id
        gr = requests.get(photo_url)
        path = gr.json()
        file_path = path['result']['file_path']
        photo = URL1 + file_path
        urlretrieve(photo, "local-filename.jpg")
        answer = CatOrDog.cat_or_dog()
        send = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, answer)
        requests.get(send)
    else:
        pass

def get_updates():
    url = URL+ 'getupdates'
    print(url)
    r = requests.get(url)
    return r.json()

def main():
    while True:
        data = get_updates()
        PhotoGet(data)
        if 0xFF == 27:
            break

if __name__ == '__main__':
    main()