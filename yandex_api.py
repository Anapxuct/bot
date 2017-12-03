import requests

# key_api = тут должен быть ключ


def translate_text(text, lang):
    """
    Перевод исходного текста.
    :param text: исходный текст.
    :param lang: исходный язык - язык перевода (ru-en).
    :return: переведенный текст.
    """
    try:
        res = requests.get(
            'https://translate.yandex.net/api/v1.5/tr.json/translate',
            params={'key': key_api, 'text': text,
                    'lang': lang})
        data = res.json()
        return data['text'][0]
    except Exception as e:
        print('Exception(translate):', e)
