import requests
from constants import OPEN_WEATHER_BASE_URL, OPEN_WEATHER_BASE_PARAMS


def get_weather(lat: float, lon: float):
    if lat is None or lon is None:
        return
    params = OPEN_WEATHER_BASE_PARAMS
    params['lat'] = lat
    params['lon'] = lon
    response = requests.get(OPEN_WEATHER_BASE_URL, params=params)
    return response.json()
