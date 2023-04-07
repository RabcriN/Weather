from city import get_city_name
from coordinates import get_coordinates
from exceptions import ApiServiceError, CantGetCoordinates, InputChoiceError
from weather_api_service import get_weather, get_weather_in_city


def get_program_mode() -> str:
    program_mode = ''
    while program_mode not in ('1', '2'):
        print(
            'Для получения погоды по текущей геопозиции, '
            'введите "1" и нажмите Enter.'
        )
        print(
            'Если хотите узнать погоду в другом населённом пункте, '
            'введите "2" и нажмите Enter.'
        )
        program_mode = str(input())
    return str(program_mode)


def start_program(program_mode: str) -> None:
    modes = {
        '1': from_coordinates,
        '2': from_city_name,
    }
    return modes[program_mode]()


def from_coordinates():
    try:
        coordinates = get_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить координаты')
        raise CantGetCoordinates
    try:
        return get_weather(coordinates)
    except ApiServiceError:
        print(f'Не удалось получить погоду по координатам {coordinates}')
        raise ApiServiceError


def from_city_name():
    city = get_city_name()
    try:
        return get_weather_in_city(city)
    except ApiServiceError:
        print(f'Не удалось получить погоду в городе {city}')
        raise ApiServiceError


def lets_try_again() -> bool:
    answer = ''
    print()
    while answer not in ('1', '2'):
        print(
            'Для повторного поиска '
            'введите "1" и нажмите Enter.'
        )
        print(
            'Для завершения программы  '
            'введите "2" и нажмите Enter.'
        )
        answer = str(input())
    if answer == '1':
        return True
    if answer == '2':
        return False
    raise InputChoiceError
