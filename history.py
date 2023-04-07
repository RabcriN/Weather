from datetime import datetime
from pathlib import Path

from weather_api_service import Weather
from weather_formatter import format_weather


class WeatherStorage:
    """Interface for saving weather data storage"""
    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage(WeatherStorage):
    """Store Weather in plain text file"""
    def __init__(self, file: Path):
        self.file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open(self.file, 'a') as f:
            f.write(f'{now}\n{formatted_weather}\n')


def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """Saves Weather in Storage"""
    storage.save(weather)
