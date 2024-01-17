import json
import time
import requests

def request_data():
    token = "df116b67df116b67df116b6725dc07ab97ddf11df116b67ba9dc54dc59cb79bed1dbf00"
    version = 5.92
    domain = "its_my_planner"
    count = 100
    offset = 0
    all_posts = []

    while offset < 1000:
        response = requests.get("https://api.vk.com/method/wall.get", params={
            'access_token': token,
            "v": version,
            'domain': domain,
            'count': count,
            'offset': offset
        })
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
        time.sleep(0.5)
    # all_posts.reverse()
    return all_posts

def write_to_json(all_posts):
    result_data = []
    for post in all_posts:
        try:
            if post['attachments'][0]['type']:
                img_url = post['attachments'][0]['photo']["sizes"][-1]['url']
            else:
                img_url = 'pass'
        except:
            pass
        text = post['text'].replace(" ", "—")
        # text = post['text'].replace("——", "—")
        text.replace("——", "—")
        result_data.append({
            "text": text,
            "IMG": img_url
        })

    with open("its_my_planner.json", "w", encoding='utf-8') as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

all_posts = request_data()
write_to_json(all_posts)

import json
import sys


# Открываем JSON-файл для чтения
with open("its_my_planner.json", "r", encoding='utf-8') as json_file:
    data = json.load(json_file)

# Перебираем элементы JSON-структуры
for i in range(len(data) - 1):
    current_item = data[i]
    next_item = data[i + 1]

    text_current = current_item["text"].replace("? ", "")
    img_url_current = current_item["IMG"]

    text_next = next_item["text"].replace("? ", "")
    img_url_next = next_item["IMG"]

    # Проверка на одинаковые ссылки и больший текст
    if img_url_current == img_url_next and len(text_current) > len(text_next):
        print("Текст:", text_current)
        print("Ссылка:", img_url_current)
        print("--------")
    else:
        # Вывод обычных данных
        print("Текст:", text_current)
        print("Ссылка:", img_url_current)
        print("--------")
