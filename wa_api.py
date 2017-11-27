import requests

API_key = 'THTGGX-JRXH63GE3V'


def get_img_answer(question):
    """
    Создает изображение ответа на question из вольфрамальфа.
    """
    res = requests.get('http://api.wolframalpha.com/v1/simple',
                       params={'appid': API_key,
                               'i': question})
    with open('img.jpg', 'wb') as out:
        out.write(res.content)

