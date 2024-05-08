import telebot
from telebot.types import Message
from supabase_conf import get_location, set_location
from constants import Callbacks, Verdicts, Commands, WeatherConditions, BOT_TOKEN
from keyboards import get_start_keyboard, get_location_keyboard
from helpers import calculate_overall_coefficient
from api import get_weather

bot = telebot.TeleBot(BOT_TOKEN)


def get_verdict(lat, lon):
    weather_data = get_weather(lat, lon)['current']
    temp = round(float(weather_data['temp']), ndigits=2)
    wind = round(float(weather_data['wind_speed']), ndigits=1)
    humidity = int(weather_data['humidity'])
    sky = weather_data['weather'][0]['description']
    weather_info = 'В вашем городе: {0} \nТемпература: {1}\nВлажность: {2} %\nВетер: {3} м/с\n'.format(sky, temp,
                                                                                                       humidity, wind)
    result = calculate_overall_coefficient(temp, humidity)

    if result > WeatherConditions.HOT:
        verdict = Verdicts.HOT
    elif result > WeatherConditions.MEDIUM:
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
        keyboard = get_start_keyboard()
        response_text = 'Привет! Я бот, который поможет тебе узнать погоду в твоем городе, а также расскажет как одеться по погоде. Чтобы начать выбери одну из кнопок. Если ты хочешь узнать погоду в своем городе, то отправь мне свою геопозицию - {0}'.format(
            Commands.LOCATION)
    elif text == Commands.LOCATION:
        keyboard = get_location_keyboard()
        response_text = 'Пришлите вашу геопозицию'
    elif text == Commands.HELP:
        response_text = '{0} - информация о погоде в твоем городе'.format(Commands.WEATHER)
    elif text == Commands.WEATHER:
        lat, lon = get_location(chat_id)
        response_text = get_verdict(lat, lon)
    else:
        response_text = 'Я тебя не понимаю. Напиши `{0}`'.format(Commands.HELP)
    send_response(user_id, response_text, keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message: Message):
    chat_id = message.chat.id
    set_location(chat_id, message.location.latitude, message.location.longitude)
    send_response(chat_id, 'Геопозиция успешно обновлена!')


call_data_variants = [
    {
        'variant': Callbacks.CITY_INFO,
        'text': 'Что хочешь?',
        'keyboard': get_location_keyboard()
    },
    {
        'variant': Callbacks.CITY_CURRENT,
        'text': 'Выбранный город'  # TODO дописать город
    },
    {
        'variant': Callbacks.CITY_CHANGE,
        'text': 'Напишите свой город или пришлите вашу геопозицию'
    }
]


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    keyboard = None
    response_text = ''
    for variant in call_data_variants:
        if call.data == variant['variant']:
            response_text = variant['text']
            if 'keyboard' in variant:
                keyboard = variant['keyboard']
            break
    send_response(call.message.chat.id, response_text, keyboard)


bot.polling(none_stop=True, interval=0)
