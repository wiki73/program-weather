from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")

OPEN_WEATHER_UNITS = 'metric'
OPEN_WEATHER_LANG = 'ru'


class Callbacks(Enum):
    CITY_INFO = 'CITY_INFO'
    CITY_CURRENT = 'CITY_CURRENT'
    CITY_CHANGE = 'CITY_CHANGE'


class Verdicts(Enum):
    HOT = 'Вердикт: Жарко. Можно и в шортах',
    WARM = 'Вердикт: Тепло. Кофта не помешает',
    MEDIUM = 'Вердикт: Средне. Кофта не помешает',
    COLD = 'Вердикт: Холодно. Советую взять куртку!'

# ctrl + R a shortcut to replace string
# ctrl + G a shortcut to select specific line
