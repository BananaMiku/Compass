import requests
import config
import keys
import location_calculations as lc

def get_bars(cur_location, radius):
    if config.TEST:
        print("TEST MODE")
        return config.MOCK_PLACE_DATA
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": keys.PLACES_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
    }
    payload = {
        "includedTypes": ["bar"],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": cur_location['lat'],
                    "longitude": cur_location['lng']
                },
                "radius": radius
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def find_closest_bar(bars, cur_location):
    if 'places' not in bars:
        print("malformed api res 🍺")
        return None
    cur_closest = None
    dist = float('inf')
    for bar in bars['places']:
        bar_cords = extract_lat_lng(bar)
        bar_dist = lc.get_distance(cur_location, bar_cords) 
        if bar_dist <= dist:
            cur_closest = bar
            dist = bar_dist
        print(cur_closest, bar)
    print(dist)
    return cur_closest
        
def extract_lat_lng(google_res):
    if 'location' not in google_res:
        return None
    return {'lat': google_res['location']['latitude'], 'lng': google_res['location']['longitude']}

def test():
    cur_location = {'lat': 42.2743676, 'lng': -72.6594507}
    bars = get_bars(cur_location, 16093.44)
    print(bars)
    print(find_closest_bar(bars, cur_location))

if __name__ == '__main__':
    test()
