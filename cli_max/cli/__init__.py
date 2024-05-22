import requests
import typer
import os
import json
import plotext as plt
from datetime import datetime


app = typer.Typer()
_debug: bool = False

GEONAMES_USERNAME = os.getenv('CLI_MAX_GEONAMES_USERNAME', 'fhg_aztek')
CACHE_DIR = os.getenv('CLI_MAX_CACHE', ".cache")
GEO_CACHE_FILE = os.path.join(CACHE_DIR, "coordinates_cache.json")

# Load cache from file if it exists
if os.path.exists(GEO_CACHE_FILE):
    with open(GEO_CACHE_FILE, 'r') as f:
        coordinates_cache = json.load(f)
else:
    coordinates_cache = {}

@app.callback(no_args_is_help=True)
def callback(debug: bool = False):
    global _debug
    _debug = debug

@app.command()
def hello(name: str):
    """Simple program that greets NAME."""
    print(f"Hello, {name}!")

def save_cache():
    """Save the coordinates cache to a file."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(GEO_CACHE_FILE, 'w') as f:
        json.dump(coordinates_cache, f)

def get_coordinates(location: str):
    """Fetch coordinates for a given location using GeoNames, with caching."""
    if location in coordinates_cache:
        if _debug:
            typer.echo(f"Using cached coordinates for {location}")
        return coordinates_cache[location]

    typer.echo(f"Fetching coordinates for {location}")
    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": location,
        "maxRows": 1,
        "username": GEONAMES_USERNAME
    }
    response = requests.get(url, params=params)
    
    if _debug:
        typer.echo(f"Response status code: {response.status_code}")
        typer.echo(f"Response content: {response.content}")

    if response.status_code == 200 and response.json().get('geonames'):
        data = response.json()['geonames'][0]
        lat_lon = (float(data['lat']), float(data['lng']))
        coordinates_cache[location] = lat_lon
        save_cache()
        typer.echo(f"Coordinates for {location}: {lat_lon[0]}, {lat_lon[1]}")
        return lat_lon
    else:
        typer.echo("Could not find location coordinates.")
        raise typer.Exit()

@app.command(no_args_is_help=True)
def weather(location: str, hours: int = 24):
    """Fetch the weather for a given location from yr.no for the specified number of hours."""
    lat, lon = get_coordinates(location)
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {
        'User-Agent': 'cli-max 0.1',
        'From': 'fhg@aztek.no'
    }
    response = requests.get(url, headers=headers)
    if _debug:
        typer.echo(f"Weather API response status code: {response.status_code}")
        typer.echo(f"Weather API response content: {response.content}")
    if response.status_code == 200:
        data = response.json()
        timeseries = data['properties']['timeseries']
        entries = timeseries[:hours]
        times = [entry['time'] for entry in entries]
        temperatures = [entry['data']['instant']['details']['air_temperature'] for entry in entries]
        
        # Print temperatures to the command line
        for time, temp in zip(times, temperatures):
            print(f"At {time}, the temperature is {temp}°C.")

        # Plot temperatures
        times = [datetime.fromisoformat(time).strftime('%d/%m/%Y %H:%M:%S') for time in times]
        plt.date_form('d/m/Y H:M:S')
        plt.plot(times, temperatures, marker='o', label='Temperature')
        plt.title(f'Temperature forecast for {location}')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.show()
    else:
        print("Failed to fetch weather data.")


if __name__ == "__main__":
    app()