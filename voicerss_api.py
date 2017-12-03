import requests

# api_key = тут должен быть ключ


def create_ogg_from_text(text):
    """
    Создать аудио файл с расширением ogg.
    :param text: текст, произносящийся в создаваемом файле.
    """
    res = requests.get('http://api.voicerss.org',
                       params={'key': api_key, 'src': text, 'hl': 'ru-ru',
                               'c': 'OGG'})
    with open('voice.ogg', 'wb') as out:
        out.write(res.content)


