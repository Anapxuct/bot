import requests

key_api = 'trnsl.1.1.20171112T134725Z.a7b47af0b6a94cfa.25a33c332c8c97681c7d8fb\
423933937f3e4f7b9'


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
