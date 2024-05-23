import requests


def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    response.raise_for_status()
    return response.text
