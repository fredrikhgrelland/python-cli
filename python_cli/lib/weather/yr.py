import requests
import os
import json

GEONAMES_USERNAME = os.getenv('CLI_GEONAMES_USERNAME', 'fhg_aztek')
CACHE_DIR = os.getenv('CLI_CACHE', ".cache")
GEO_CACHE_FILE = os.path.join(CACHE_DIR, "coordinates_cache.json")

# Load cache from file if it exists
if os.path.exists(GEO_CACHE_FILE):
    with open(GEO_CACHE_FILE, 'r') as f:
        coordinates_cache = json.load(f)
else:
    coordinates_cache = {}

def save_cache():
    """Save the coordinates cache to a file."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(GEO_CACHE_FILE, 'w') as f:
        json.dump(coordinates_cache, f)

def location_forecast(lat, lon):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {
        'User-Agent': 'cli 0.1',
        'From': 'fhg@aztek.no'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_coordinates(location: str, search_type:str = "searchJSON"):
    """Fetch coordinates for a given location using GeoNames, with caching."""
    if location in coordinates_cache:
        return coordinates_cache[location]

    url = f"http://api.geonames.org/{search_type}"
    params = {
        "q": location,
        "maxRows": 1,
        "username": GEONAMES_USERNAME
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    if response.status_code == 200 and response.json().get('geonames'):
        data = response.json()['geonames'][0]
        lat_lon = (float(data['lat']), float(data['lng']))
        coordinates_cache[location] = lat_lon
        save_cache()
        return lat_lon
    elif search_type != "wikipediaSearchJSON":
        return get_coordinates(location, search_type="wikipediaSearchJSON")
    raise ValueError(f"Could not find coordinates for {location}")


def get_weather(location: str, hours: int = 1, return_json: bool = False):
    lat, lon = get_coordinates(location)
    forecast = location_forecast(lat, lon)
    timeseries = forecast['properties']['timeseries']
    entries = timeseries[:hours]
    times = [entry['time'] for entry in entries]
    temperatures = [entry['data']['instant']['details']['air_temperature'] for entry in entries]  
    if return_json:
        return {
            "times": times,
            "temperatures": temperatures
        }
    _output = f"Weather forecast for {location}:\n"
    for time, temp in zip(times, temperatures):
        _output += f"At {time}, the temperature is {temp}°C.\n"
    return _output