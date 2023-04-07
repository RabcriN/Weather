import json
from datetime import datetime
from enum import Enum
from json.decoder import JSONDecodeError
from typing import NamedTuple, Union

import requests
from typing_extensions import Literal

from constants import OPEN_WEATHER_URL_BY_CITY, OPEN_WEATHER_URL_BY_GPS
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    location: str
    feels_like: Celsius


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather from openweather API and returns it"""
    openweather_response = _get_openweather_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather


def get_weather_in_city(city: str) -> Weather:
    """Requests weather from openweather API and returns it"""
    openweather_response = _get_openweather_response_in_city(city)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response_in_city(city: str) -> bytes:
    url = OPEN_WEATHER_URL_BY_CITY.format(city=city)
    if requests.get(url).status_code == 404:
        raise ApiServiceError
    try:
        return requests.get(url).content
    except Exception:
        raise ApiServiceError


def _get_openweather_response(latitude: float, longitude: float) -> bytes:
    url = OPEN_WEATHER_URL_BY_GPS.format(
        latitude=latitude, longitude=longitude
    )
    try:
        return requests.get(url).content
    except Exception:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: bytes) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperatures(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        location=_parse_location(openweather_dict),
        feels_like=_parse_feels_like(openweather_dict),
    )


def _parse_temperatures(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_feels_like(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['feels_like'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(
    openweather_dict: dict,
    time: Union[Literal['sunrise'], Literal['sunset']]
) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_location(openweather_dict: dict) -> str:
    try:
        return openweather_dict['name']
    except (KeyError):
        raise ApiServiceError
