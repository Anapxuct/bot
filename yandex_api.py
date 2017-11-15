import requests

# key_api =  тут должен быть ключ


def translate_text(text, lang):
    try:
        res = requests.get(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            params={'key': key_api, 'text': text,
                    'lang': lang})
        data = res.json()
        return data['text'][0]
    except Exception as e:
        print('Exception(translate):', e)
