import requests
import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from supabase_conf import supabase

bot = telebot.TeleBot('6812718555:AAFDyqCMLX_CUnB8vg-U24Kb3B7sMT5YS-U')

CHECK_CITY = 'check_city'
CHANGE = 'change'


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


def get_location(id):
    response = supabase.table('users').select('lat', 'lon').eq('id', id).execute()
    lat = round(float(response.data[0]['lat']), ndigits=2)
    lon = round(float(response.data[0]['lon']), ndigits=2)
    print(lat, lon)
    return lat, lon


# https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid=79d1ca96933b0328e1c7e3e7a26cb347
# https://api.openweathermap.org/data/3.0/
# ?lat=50.18&lon=39.62&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347
def get_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/3.0/onecall?lat={0}&lon={1}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'.format(
        lat, lon)
    weather_data = requests.get(url).json()['current']
    temp = round(float(weather_data['temp']), ndigits=2)
    wind = round(float(weather_data['wind_speed']), ndigits=1)
    humidity = int(weather_data['humidity'])
    sky = weather_data['weather'][0]['description']
    weather_info = 'В вашем городе: {0} \nТемпература: {1}\nВлажность: {2} %\nВетер: {3} м/с\n'.format(sky, temp,
                                                                                                       humidity, wind)
    print(weather_info)
    value_3 = calculate_overall_coefficient(21, 40)
    value_2 = calculate_overall_coefficient(14, 60)
    v = calculate_overall_coefficient(temp, humidity)
    if v > value_3:
        verdict = 'Вердикт: Жара. Одевайся легко'
    elif v > value_2:
        verdict = 'Вердикт: Средне. Кофта не помешает'
    else:
        verdict = 'Вердикт: Холодно. Советую взять куртку!'
    return weather_info + verdict


# ctrl + R a shortcut to replace string
# ctrl + G a shortcut to select specific line

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if not isinstance(message, Message):
        return
    if message.text.lower() == "п" or message.text.lower() == "погодка":
        lat, lon = get_location(message.chat.id)
        a = get_weather(lat, lon)
        bot.send_message(message.from_user.id, a)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Погодка")
    elif message.text == "/start":
        keyboard = InlineKeyboardMarkup()
        key_city = InlineKeyboardButton(text='Город', callback_data='city')
        keyboard.add(key_city)
        key_no = InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text='Настройки', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Напиши Погодка")


@bot.message_handler(content_types=['location'])
def handle_location(message):
    if isinstance(message, Message):
        chat_id = message.chat.id
        lat = message.location.latitude
        lon = message.location.longitude
        print("{0}, {1}".format(lat,
                                lon))
        existing_user = supabase.table('users').select('*').eq('id', chat_id).execute().data
        if not len(existing_user) > 0:
            supabase.table('users').insert({"id": chat_id, 'lat': lat, 'lon': lon}).execute()
            bot.send_message(chat_id, 'Геопозиция успешно добавлена!')
        else:
            supabase.table('users').update({'lat': lat, 'lon': lon}).eq("id", chat_id).execute()
            bot.send_message(chat_id, 'Геопозиция успешно обновлена!')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    if call.data == "city":
        keyboard = InlineKeyboardMarkup()
        key_check_city = InlineKeyboardButton(text='Посмотреть выбранный город', callback_data=CHECK_CITY)
        keyboard.add(key_check_city)
        key_no = InlineKeyboardButton(text='Изменить город', callback_data=CHANGE)
        keyboard.add(key_no)
        bot.send_message(chat_id, 'Что хочешь?', reply_markup=keyboard)
    elif call.data == CHECK_CITY:
        bot.send_message(chat_id, f'Выбранный город ')  # TODO дописать город
    elif call.data == CHANGE:
        bot.send_message(chat_id, f'Напишите свой город или пришлите вашу геопозицию')


bot.polling(none_stop=True, interval=0)
