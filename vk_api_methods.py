import vk_api
import random
import requests
from flask import json

vk = vk_api.VkApi(token='d255cecd1007c7276bae7e0c1684ec3e3b94a18f778e5bdcfb7f3\
8846507a023e0228e937385f0da8f7c5')
vk._auth_token()
values = {'out': 0, 'count': 20, 'time_offset': 10}


def get_msgs():
    """ Возвращает словарь сообщений.
    Получить список сообщений.
    """
    msgs = vk.method('messages.get', values)
    for item in msgs['items']:
        if 'chat_id' not in item:
            item['chat_id'] = 0
    return msgs


def write_msg_in_chat(chat_id, user_id, msg):
    """
    Написать сообщение msg в беседу chat_id или пользователю user_id, если
    chat_id = 0.
    """
    if chat_id == 0:
        vk.method('messages.send', {'user_id': user_id, 'message': msg})
    else:
        vk.method('messages.send', {'chat_id': chat_id, 'message': msg})


def chose_user(chat_id):
    """ Возвращает словарь из id, имени и фамилии.
    Выбор произвольного человека из беседы chat_id.
    """
    ids = vk.method('messages.getChatUsers', {'chat_id': chat_id,
                                              'fields': 'nickname'})
    ids = [id for id in ids if id['id'] != 439872373]
    user = ids[random.randint(0, len(ids) - 1)]
    return user


def send_ref(chat_id, user_id):
    """
    Отправляет справку в беседу chat_id или пользователю user_id, если
    chat_id = 0.
    """
    ref = 'Чтобы обратиться ко мне начни сообщение с "Бот Котя"\n' + \
          u'\u2713' + 'привет, чтобы поздоровоться со мной\n' + \
          u'\u2713' + 'кто "любая_фраза" - выбрать пользователя из группы,\
           который "любая_фраза\n' + \
          u'\u2713' + 'send "что-либо" - написать что-либо в беседу\n' + \
          u'\u2713' + 'вероятность "фраза" - вероятность того, что "фраза" -\
           правда\n' \
          + u'\u2713' + 'выбор ... или ... или ... - помочь с выбором из любого\
           кол-ва вариантов\n' + \
          u'\u2713' + 'погода Название_города - погода в данный момент\n' + \
          u'\u2713' + 'прогноз Название_города на n - прогноз погоды на n \
          дней' + '\n' + u'\u2713' + 'когда "событие" - когда произойдет \
          событие\n' + u'\u2713' + 'вольфрам "запрос" - получить ответ с \
          wolframalpha\n' + u'\u2713' + 'транслит "сообщение" - изменить \
          раскладку сообщения'

    write_msg_in_chat(chat_id, user_id, ref)


def send_msg(chat_id, user_id, msg):
    """
    Написать заданное сообщение msg в беседу chat_id.
    """
    msg = 'Бот Котя: ' + msg[msg.index('send') + 4:].lstrip()
    write_msg_in_chat(chat_id, user_id, msg)


def choice(chat_id, user_id, msg):
    """
    Выбрать один из двух вариантов, разделенных 'или' и отправить сообщением.
    """
    msg = msg.split('или')
    msg[0] = msg[0][msg[0].index('выбор') + 5:]
    for i in range(1, len(msg)):
        msg[i] = msg[i].lstrip()
    write_msg_in_chat(chat_id, user_id, 'Бот Котя: ' +
                      msg[random.randint(0, len(msg) - 1)].lstrip())


def send_photo(chat_id, user_id, photo_name):
    """
    Отправить фото сообщением.
    """
    server = vk.method('photos.getMessagesUploadServer')
    upload_url = server['upload_url']
    img = {'photo': (photo_name, open(photo_name, 'rb'))}
    response = requests.post(upload_url, files=img)
    result = json.loads(response.text)
    print('2:', result)
    try:
        saved_photo = vk.method('photos.saveMessagesPhoto',
                                {'photo': result['photo'],
                                 'hash': result['hash'],
                                 'server': result['server']})
        photo = 'photo' + str(saved_photo[0]['owner_id']) + '_' \
                + str(saved_photo[0]['id'])
        if chat_id == 0:
            vk.method('messages.send', {'user_id': user_id,
                                        'attachment': photo})
        else:
            vk.method('messages.send', {'chat_id': chat_id,
                                        'attachment': photo})
    except Exception as e:
        print('Exception(send_photo)', e)
        write_msg_in_chat(chat_id, user_id, 'Что-то пошло не так :С')
