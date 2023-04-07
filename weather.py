from pathlib import Path

from exceptions import ApiServiceError, CantGetCoordinates, InputChoiceError
from history import PlainFileWeatherStorage, save_weather
from program_mode import get_program_mode, lets_try_again, start_program
from weather_formatter import format_weather


def main():
    mode = get_program_mode()
    try:
        weather = start_program(mode)
    except (ApiServiceError, CantGetCoordinates, InputChoiceError):
        if lets_try_again():
            main()
        print('Всего наилучшего!')
        return exit(1)

    print(format_weather(weather))
    save_weather(
        weather,
        PlainFileWeatherStorage(Path.cwd() / 'weather_history.txt')
    )
    if lets_try_again():
        main()
    print('Всего наилучшего!')
    return exit(1)


if __name__ == "__main__":
    main()
