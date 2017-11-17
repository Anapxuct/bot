from re import search
import random
import vk_api_methods as vk
import openweathermap_api as weather_api
import datetime


def when_it_happend(item):
    """Сказать, когда произойдет событие"""
    today_date = datetime.date.today()
    random_date = today_date + datetime.timedelta(random.randint(1, 20 * 365))
    msg = item['body'][item['body'].index('когда') + 5:].lstrip() + ' ' \
          + random_date.isoformat()
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)


def say_hello(item):
    """Сказать привет"""
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], 'Привет!')


def chance(item):
    """Написать вероятность события"""
    msg = 'Вероятность того, что ' \
          + item['body'][item['body'].index('вероят') + 11:].lstrip() + ' ' \
          + str(random.randint(1, 100)) + '%'
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)


def send(item):
    """Написать что-то в чат"""
    vk.send_msg(item['chat_id'], item['user_id'], item['body'])


def who_is(item):
    """Выбрать пользователя из списка участников группы"""
    if item['chat_id'] == 0:
        vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                             'Эта функция доступна только в беседах.')
    else:
        user = vk.chose_user(item['chat_id'])
        msg = '@id' + str(user['id']) + ' (' + user['first_name'] + ' ' \
              + user['last_name'] + ') ' \
              + item['body'][item['body'].index('кто') + 3:].lstrip()
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)


def current_weather(item):
    """Написать текущую погоду в городе"""
    pattern_with_country = r' погода \w+,\w+'
    pattern_without_country = r' погода \w+'

    if search(pattern_with_country, item['body']) \
            or search(pattern_without_country, item['body']):
        name_of_city = item['body'][item['body'].index('погода') + 6:].lstrip()
        weather = weather_api.get_weather_of_city(name_of_city)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], weather)
    else:
        vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                             'Я не поняль :С')


def weather_forecast(item):
    """Написать прогноз погоды на несколько дней"""
    pattern_with_country = r' прогноз \w+,\w+ на \d\s*$'
    pattern_without_country = r' прогноз \w+ на \d\s*$'

    if (search(pattern_with_country, item['body'])
        or search(pattern_without_country, item['body'])) \
            and item['body'][-1].isdigit():
        ind_before = item['body'].index('прогноз') + 7
        ind_after = item['body'].index('на')

        name_of_city = (item['body'][ind_before:ind_after].lstrip()).rstrip()

        days = int(item['body'][item['body'].index('на') + 3])
        if 0 < days < 6:
            forecast = weather_api.get_weather_forecast(name_of_city,
                                                        days)
            vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                                 forecast)
        else:
            vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                                 'Я могу сказать погоду только на 1-5 \
                                 дней')
    else:
        vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                             'Я не поняль :С')


def chose(item):
    """Выбрать из нескольких вариантов"""
    vk.choice(item['chat_id'], item['user_id'], item['body'])


def send_help(item):
    """Отправить справку в чат"""
    vk.send_ref(item['chat_id'], item['user_id'])
