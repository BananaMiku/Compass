import requests
import config
import keys
import location_calculations as lc

def get_bars(cur_location, radius):
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
        cur_cords = extract_lat_lng(cur_closest) if cur_closest != None else None
        bar_dist = lc.get_distance(cur_cords, bar_cords) 
        if bar_dist <= dist:
            cur_closest = bar
            dist = bar_dist
        print(bar_dist, bar)
    print(dist)
    return cur_closest
        
def extract_lat_lng(google_res):
    if 'location' not in google_res:
        return None
    return {'lat': google_res['location']['latitude'], 'lng': google_res['location']['longitude']}

def test():
    cur_location = {'lat': 42.3894, 'lng':  -72.5265 }
    bars = get_bars(cur_location, 16093.44)
    print(bars)
    print(find_closest_bar(bars, cur_location))

if __name__ == '__main__':
    test()
