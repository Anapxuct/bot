import requests
import pickle
from yandex_api import translate_text

app_id = "88063fe5009f859f9523718cf06d539e"


def get_city_id(name_of_city):
    """
    Получение id города, если он не был получен ранее .
    """
    with open('cities for weather', 'rb') as f:
        cities = pickle.load(f)
    if name_of_city in cities:
        return cities[name_of_city]
    else:
        try:
            en_name_of_city = translate_text(name_of_city, 'ru-en')
            if 'oe' in en_name_of_city:
                en_name_of_city = en_name_of_city.replace('oe', 'oye')
            print(en_name_of_city)
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': en_name_of_city, 'type': 'accurate',
                                       'lang': 'ru',
                                       'units': 'metric', 'APPID': app_id})
            data = res.json()
            for d in data['list']:
                cities[name_of_city] = d['id']
            with open('cities for weather', 'wb') as f:
                pickle.dump(cities, f)
            return cities[name_of_city]
        except Exception as e:
            print("Exception (find):", e)


def get_weather_of_city(name_of_city):
    """
    Возвращает погодные условия и температуру в городе в данный момент.
    """
    city_id = get_city_id(name_of_city)
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric',
                                   'lang': 'ru', 'APPID': app_id})
        data = res.json()
        weather = 'Погодные условия: {} \nТемпература: {} \nТемпература от {} \
        до {} градусов'.format(data['weather'][0]['description'],
                               data['main']['temp'], data['main']['temp_min'],
                               data['main']['temp_max'])
        return weather
    except Exception as e:
        print("Exception (weather):", e)
        return 'Не могу найти такой город :С'


def get_weather_forecast(name_of_city, days):
    """
    Возвращает прогноз погоды на days дней с интервалом в 3 часа.
    """
    city_id = get_city_id(name_of_city)
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric',
                                   'lang': 'ru', 'APPID': app_id})
        data = res.json()
        print(data)
        forecast = ''
        for i in range(0, days * 8, 2):
            forecast += data['list'][i]['dt_txt'] + ': температура {}, погодные \
            условия: '.format(data['list'][i]['main']['temp']) \
                        + data['list'][i]['weather'][0]['description'] \
                        + '\n'
        return forecast
    except Exception as e:
        print("Exception (forecast):", e)
        return 'Не могу найти такой город :С'
