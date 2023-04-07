import tkinter as tk
from coordinates import get_coordinates, get_ip
from weather_api_service import get_weather, get_weather_in_city
from weather_formatter import format_weather
from exceptions import ApiServiceError


def get_my_weather():
    city = input_field.get()
    if city:
        try:
            weather = get_weather_in_city(city)
            text = format_weather(weather)
            weather_label.config(
                    text=text
                )
        except ApiServiceError:
            weather_label.config(
                    text=(f'Не удалось найти погоду в городе {city}')
                )
    else:
        weather_label.config(
                    text=('Необходимо ввести название города')
                )


def get_location_weather():
    coordinates = get_coordinates()
    weather = get_weather(coordinates)
    text = format_weather(weather)
    weather_label.config(
        text=text
    )


root = tk.Tk()
root.title("Приложение прогноза погоды")
root.geometry("400x200")

input_label = tk.Label(root, text="Введите название города:")
input_label.pack()

input_field = tk.Entry(root)
input_field.pack()

submit_button = tk.Button(
    root,
    text="Узнать погоду в городе",
    command=get_my_weather
)
submit_button.pack()

ip = get_ip()
input_label = tk.Label(root, text=f"Ваш текущий IP: {ip}")
input_label.pack()

location_button = tk.Button(
    root,
    text="Узнать погоду по IP",
    command=get_location_weather
)
location_button.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

root.mainloop()
