import json


def load_json():
    with open('config/books.json', 'r') as f:
        data = json.load(f)
        return data


def save_Json(data):
    with open("config/books.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
