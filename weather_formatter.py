from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Formats Weather data into string"""
    return (
        f'Ваша локация: {weather.location}\n'
        f'Температура: {weather.temperature}°С, '
        f'{weather.weather_type.value}\n'
        f'Ощущается как: {weather.feels_like}°С\n'
        f'Восход: {weather.sunrise.strftime("%H:%M")}\n'
        f'Закат: {weather.sunset.strftime("%H:%M")}\n'
    )
