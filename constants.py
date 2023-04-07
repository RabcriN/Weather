from secrets import API_KEY

OPEN_WEATHER_URL_BY_GPS = (
    'https://api.openweathermap.org/data/2.5/weather?'
    'lat={latitude}&lon={longitude}&'
    'appid=' + API_KEY + '&lang=ru&units=metric'
)

OPEN_WEATHER_URL_BY_CITY = (
    'https://api.openweathermap.org/data/2.5/weather?'
    'q={city}&'
    'appid=' + API_KEY + '&lang=ru&units=metric'
)
