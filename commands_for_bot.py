from re import search
import random
import requests
import main_lumb as ml
import vk_api_methods as vk
import openweathermap_api as weather_api
import wa_api
import datetime
import voicerss_api as voice


def when_it_happend(item):
    """
    Сказать, когда произойдет событие.
    :param item: сообщение с командой
    """
    today_date = datetime.date.today()
    random_date = today_date + datetime.timedelta(random.randint(1, 20 * 365))
    msg = item['body'][item['body'].index('когда') + 5:].lstrip() + ' ' \
          + random_date.isoformat()
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)


def say_hello(item):
    """
    Сказать привет.
    :param item: сообщение с командой
    """
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], 'Привет!')


def chance(item):
    """
    Написать вероятность события.
    :param item: сообщение с командой
    """
    msg = 'Вероятность того, что ' \
          + item['body'][item['body'].index('вероят') + 11:].lstrip() + ' ' \
          + str(random.randint(1, 100)) + '%'
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)


def send(item):
    """
    Написать что-то в чат.
    :param item: сообщение с командой
    """
    vk.send_msg(item['chat_id'], item['user_id'], item['body'])


def who_is(item):
    """
    Выбрать пользователя из списка участников группы.
    :param item: сообщение с командой
    """
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
    """
    Написать текущую погоду в городе.
    :param item: сообщение с командой
    """
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
    """
    Написать прогноз погоды на несколько дней.
    :param item: сообщение с командой
    """
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
    """
    Выбрать из нескольких вариантов.
    :param item: сообщение с командой
    """
    vk.choice(item['chat_id'], item['user_id'], item['body'])


def send_help(item):
    """
    Отправить справку в чат.
    :param item: сообщение с командой
    """
    ref = 'Чтобы обратиться ко мне начни сообщение с "Котя"\n' + \
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
          раскладку сообщения\n' + u'\u2713' + 'день недели - узнать, какой \
          сегодня день недели\n' + u'\u2713' + 'скажи "текст" - произносит \
          "текст" в голосовом сообщении\n' + u'\u2713' + 'курс - узнать \
          курс доллара и евро\n' + u'\u2713' + 'что такое - узнать значение \
          слова\n' + u'\u2713' + 'перевод язык1 язык2 текст - перевести текст \
          с языка1 на язык2\n' + u'\u2713' + 'запомни текст - запомнить \
          текст\n' + u'\u2713' + 'напомни - вывести то, что было запомнено \
          ранее\n' + u'\u2713' + 'музыка "название трека" - ссылка на \
          скачивание трека\n'

    vk.write_msg_in_chat(item['chat_id'], item['user_id'], ref)


def wolfram_img_ans(item):
    """
    Отправить фотографию ответа из вольфрамальфа.
    :param item: сообщение с командой
    """
    question = item['body'][item['body'].index('вольфрам') + 8:].lstrip()
    wa_api.get_img_answer(question)
    vk.send_photo(item['chat_id'], item['user_id'], 'img.jpg')


def translit(item):
    """
    Сменить раскладку сообщения.
    :param item: сообщение с командой
    """
    mes = "Бот Котя: "
    alf = "qйwцeуrкtеyнuгiшoщpз[х]ъaфsыdвfаgпhрjоkлlд;ж'эzяxчcсvмbиnтmь,б.ю/."

    for ch in item['body'][item['body'].index('транслит') + 8:]:
        if ch.lower() in alf:
            if alf.index(ch.lower()) % 2 == 0:
                if ch.isupper():
                    mes += alf[alf.index(ch.lower()) + 1].upper()
                else:
                    mes += alf[alf.index(ch.lower()) + 1]
            else:
                if ch.isupper():
                    mes += alf[alf.index(ch.lower()) - 1].upper()
                else:
                    mes += alf[alf.index(ch.lower()) - 1]
        else:
            mes += ch

    vk.write_msg_in_chat(item['chat_id'], item['user_id'], mes)


def day_of_week(item):
    """
    Написать, какой сегодня день недели.
    :param item: сообщение с командой
    """
    if "день недели" not in item['body']:
        vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                             'Я не поняль :С')
        return
    days = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг',
            4: 'пятница', 5: 'суббота', 6: 'воскресенье'}
    current_date = datetime.date.today()
    day = current_date.weekday()
    mes = "Сегодня " + days[day] + ' ' + '🙃'
    vk.write_msg_in_chat(item['chat_id'], item['user_id'], mes)


def send_audio_message(item):
    """
    Отправить аудио сообщение.
    :param item: сообщение с командой
    """
    ind = item['body'].index('скажи')
    mes = item['body'][ind + 5:].lstrip()
    voice.create_ogg_from_text(mes)
    vk.send_voice_message(item['chat_id'], item['user_id'], 'voice.ogg')


def show_exchange_rates(item):
    """
    Написать курс евро и доллара США к рублю.
    :param item: сообщение с командой
    """
    try:
        res = requests.get('https://finance.rambler.ru/currencies/')
        res = res.text
        euro = res[res.index('Евро'):]
        euro = euro[euro.index('span') + 5:euro.index('</span>')]
        res = res[res.index('Доллар США'):]
        dollar = res[res.index('span') + 5:res.index('</span>')]
        msg = "Курс евро: {} руб.\nКурс доллара США: {} руб.".format(euro,
                                                                     dollar)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)
    except Exception as e:
        print('Exception(show_exchange_rates):', e)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                             'Что-то пошло не так :С')


def send_music(item):
    song_name = item['body'][item['body'].index('музыка') + 6:].lstrip()
    url = 'http://go.mail.ru/zaycev?sbmt=1512993839750'
    res = requests.get(url, params={'q': song_name})
    res = res.text
    try:
        res = res[res.index('class="result__snp"'):]
        url2 = res[res.index('http'):res.index('"><span')]
        res = requests.get(url2)
        res = res.text
        res = res[res.index('audiotrack-button__label'):]
        url_download = res[res.index('http'):res.index('" id=')]
        msg = 'Ссылка для скачивания: ' + url_download
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], msg)
    except Exception:
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], 'Не могу найти \
        такую песню :С')
        return


def wiki_lumb(item):
    if ml.checkcmdWIKI(item):
        mes = ml.Wiki(item)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], mes)


def translate_lumb(item):
    if ml.checkcmdTRANSLATE(item):
        mes = ml.Translate(item)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], mes)


def recall_lumb(item):
    if ml.checkcmdRECALL(item):
        mes = ml.Recall(item)
        vk.write_msg_in_chat(item['chat_id'], item['user_id'], mes)


def remember_lumb(item):
    if ml.checkcmdREMEMBER(item):
        ml.Remember(item)
