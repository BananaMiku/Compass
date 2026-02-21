import requests
import config

PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
def get_bars(cur_location, radius):
    if test == True:
        return

    params = {
        "key": PLACES_KEY,
        "location": cur_location,  
        "radius": radius,
        "type": "bar",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

