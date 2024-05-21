import requests
import typer

app = typer.Typer()

@app.callback(no_args_is_help=True)

@app.command()
def hello(name: str):
    """Simple program that greets NAME."""
    print(f"Hello, {name}!")

def get_coordinates(location: str):
    """Fetch coordinates for a given location using Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    else:
        typer.echo("Could not find location coordinates.")
        raise typer.Exit()

@app.command(no_args_is_help=True)
def weather(location: str):
    """Fetch the weather for a given location from yr.no."""
    lat, lon = get_coordinates(location)
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {
        'User-Agent': 'my_cli_project/1.0 (myemail@example.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        timeseries = data['properties']['timeseries']
        for entry in timeseries[:5]:  # Show the first 5 entries
            time = entry['time']
            temperature = entry['data']['instant']['details']['air_temperature']
            print(f"At {time}, the temperature is {temperature}°C.")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    app()