import time
from commands_for_bot import *

# Список доступных команд.
commands = {'привет': say_hello,
            'вероятность': chance,
            'send': send,
            'кто': who_is,
            'погода': current_weather,
            'прогноз': weather_forecast,
            'выбор': chose,
            'помощь': send_help,
            'когда': when_it_happend,
            'вольфрам': wolfram_img_ans,
            'транслит': translit}

while True:
    response = vk.get_msgs()
    # Обновляем список последних сообщений.
    if response['items']:
        vk.values['last_message_id'] = response['items'][0]['id']
    # Проверяем наличие команды для бота в каждом сообщении.
    for item in response['items']:
        if not search(r'^\s*Бот Котя\s*', item['body'])\
                or len(item['body'].split()) < 2:
            continue
        command = item['body'].split()[2].lower()
        if command in commands:
            commands[command](item)
        else:
            vk.write_msg_in_chat(item['chat_id'], item['user_id'],
                                 'Я не поняль :С')
    time.sleep(1)
