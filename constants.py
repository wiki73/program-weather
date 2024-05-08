from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

OPEN_WEATHER_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_BASE_PARAMS = {
    'units': 'metric',
    'lang': 'ru',
    'appid': OPEN_WEATHER_KEY
}


class Callbacks(Enum):
    CITY_INFO = 'CITY_INFO'
    CITY_CURRENT = 'CITY_CURRENT'
    CITY_CHANGE = 'CITY_CHANGE'
    WEATHER = 'WEATHER'
    CANCEL = 'CANCEL'


class Verdicts(Enum):
    HOT = 'Вердикт: Жарко. Можно и в шортах',
    MEDIUM = 'Вердикт: Средне. Кофта не помешает',
    COLD = 'Вердикт: Холодно. Советую взять куртку!',


class WeatherConditions(Enum):
    HOT = 0.5
    MEDIUM = 0.25


class Commands(Enum):
    START = '/start',
    HELP = '/help',
    WEATHER = '/weather',
    LOCATION = '/location',

# ctrl + R a shortcut to replace string
# ctrl + G a shortcut to select specific line
