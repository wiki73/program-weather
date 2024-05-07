import requests
import telebot
from telebot.types import Message
from supabase_conf import get_location, set_location
from constants import Callbacks, Verdicts, Commands, OPEN_WEATHER_UNITS, OPEN_WEATHER_LANG, OPEN_WEATHER_KEY, BOT_TOKEN
from keyboards import start_keyboard_buttons, location_keyboard_buttons, get_keyboard

bot = telebot.TeleBot(BOT_TOKEN)


def calculate_overall_coefficient(temperature, humidity, ):
    temperature_weight = 0.5
    humidity_weight = 0.5
    normalized_temperature = temperature / 100
    normalized_humidity = humidity / 100
    overall_coefficient = (
            (normalized_temperature * temperature_weight) /
            (normalized_humidity * humidity_weight)
    )
    return overall_coefficient


def get_weather(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'units': OPEN_WEATHER_UNITS,
        'lang': OPEN_WEATHER_LANG,
        'appid': OPEN_WEATHER_KEY
    }
    url = 'https://api.openweathermap.org/data/3.0/onecall'
    response = requests.get(url, params=params)
    weather_data = response.json()['current']
    temp = round(float(weather_data['temp']), ndigits=2)
    wind = round(float(weather_data['wind_speed']), ndigits=1)
    humidity = int(weather_data['humidity'])
    sky = weather_data['weather'][0]['description']
    weather_info = 'В вашем городе: {0} \nТемпература: {1}\nВлажность: {2} %\nВетер: {3} м/с\n'.format(sky, temp,
                                                                                                       humidity, wind)
    value_3 = calculate_overall_coefficient(21, 40)
    value_2 = calculate_overall_coefficient(14, 60)
    v = calculate_overall_coefficient(temp, humidity)
    if v > value_3:
        verdict = Verdicts.HOT
    elif v > value_2:
        verdict = Verdicts.MEDIUM
    else:
        verdict = Verdicts.COLD
    return weather_info + verdict.value


def send_response(user_id, text, reply_markup=None):
    bot.send_message(user_id, text, reply_markup=reply_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.lower().strip()
    keyboard = None
    if text == Commands.START:
        keyboard = get_keyboard(start_keyboard_buttons)
        response_text = 'Привет! Я бот, который поможет тебе узнать погоду в твоем городе, а также расскажет как одеться по погоде. Чтобы начать выбери одну из кнопок. Если ты хочешь узнать погоду в своем городе, то отправь мне свою геопозицию - {0}'.format(
            Commands.LOCATION)
    elif text == Commands.LOCATION:
        keyboard = get_keyboard(location_keyboard_buttons)
        response_text = 'Пришлите вашу геопозицию'
    elif text == Commands.HELP:
        response_text = '{0} - информация о погоде в твоем городе'.format(Commands.WEATHER)
    elif text == Commands.WEATHER:
        lat, lon = get_location(chat_id)
        response_text = get_weather(lat, lon)
    else:
        response_text = 'Я тебя не понимаю. Напиши `{0}`'.format(Commands.HELP)
    send_response(user_id, response_text, keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message: Message):
    chat_id = message.chat.id
    set_location(chat_id, message.location.latitude, message.location.longitude)
    send_response(chat_id, 'Геопозиция успешно обновлена!')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    call_data = call.data
    keyboard = None
    if call_data == Callbacks.CITY_INFO:
        keyboard = get_keyboard(location_keyboard_buttons)
        response_text = 'Что хочешь?'
    elif call.data == Callbacks.CITY_CURRENT:
        response_text = 'Выбранный город'  # TODO дописать город
    elif call.data == Callbacks.CITY_CHANGE:
        response_text = 'Напишите свой город или пришлите вашу геопозицию'
    else:
        response_text = 'Неверная команда'
    send_response(chat_id, response_text, keyboard)


bot.polling(none_stop=True, interval=0)
