from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from constants import Callbacks

start_keyboard_buttons = [
    {
        'text': 'Город',
        'callback': Callbacks.CITY_INFO
    },
    {
        'text': 'Погода',
        'callback': Callbacks.WEATHER
    },
    {
        'text': 'Отмена',
        'callback': Callbacks.CANCEL
    }
]

location_keyboard_buttons = [
    {
        'text': 'Посмотреть выбранный город',
        'callback': Callbacks.CITY_CURRENT
    },
    {
        'text': 'Изменить город',
        'callback': Callbacks.CITY_CHANGE
    }
]


def get_keyboard(buttons):
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button['text'], callback_data=button['callback']))
    return keyboard


def get_start_keyboard():
    return get_keyboard(start_keyboard_buttons)


def get_location_keyboard():
    return get_keyboard(location_keyboard_buttons)
