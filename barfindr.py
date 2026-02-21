import requests
import config
import keys

def get_bars(cur_location, radius):
    if config.TEST == True:
        return config.MOCK_PLACE_DATA
    params = {
        "key": keys.PLACES_KEY,
        "location": cur_location,  
        "radius": radius,
        "type": "bar",
    }
    response = requests.get(config.PLACES_URL, params=params)
    data = response.json()
    return data

def find_closest_bar(bars, cur_location):
    if bars.status != 200 or 'results' not in bars:
        print("malformed api res 🍺")
        return None
    cur_closest = None
    dist = float('inf')
    for bar in bars['results']:
        bar_cords = extract_lat_long(bar)
        bar_dist = get_distance(cur_location, bar_cords) 
        if bar_dist <= dist:
            cur_closest = bar_cords
            dist = bar_dist
    return cur_closest
        
def extract_lat_lng(google_res):
    if 'geometry' not in google_res or 'location' not in google_res['geometry']:
        return none
    return [google_res['geometry']['location']['lat'], google_res['geometry']['location']['lng']]

def test():
    bars = get_bars([0, 0], 1500)
    print(find_closest_bar(bars, [0,0] ))

if __name__ == '__main__':
    test()
