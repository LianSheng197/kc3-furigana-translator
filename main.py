import pykakasi
import json

kks = pykakasi.kakasi()

with open("quotes.json", encoding='utf-8-sig') as json_data:
    data = json.load(json_data)


def modify_json(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = modify_json(value)
    elif isinstance(obj, list):
        return [modify_json(item) for item in obj]
    elif isinstance(obj, str):
        # Only convert string type
        return convert_kanji_to_hiragana(obj)
    else:
        return obj

    return obj


def convert_kanji_to_hiragana(text):
    result = []
    for item in kks.convert(text):
        if item['orig'] == item['hira']:
            result.append(item['orig'])
        else:
            c = ""
            c += "<ruby>"
            c += f"{item['orig']}"
            c += "<rp>(</rp>"
            c += f"<rt>{item['hira']}</rt>"
            c += "<rp>)</rp>"
            c += "</ruby>"
            result.append(c)

    output = ''.join(result)

    return output


output = modify_json(data)

with open('translated.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
