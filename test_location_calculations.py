import location_calculations

def test_distance():
    new_york = {"lat": 40.7128, "lng": -74.0060}
    boston = {"lat": 42.3601, "lng": -71.0589}
    distance = location_calculations.get_distance(new_york, boston)
    assert distance > 300_000 and distance < 350_000

def test_bearing():
    new_york = {"lat": 40.7128, "lng": -74.0060}
    boston = {"lat": 42.3601, "lng": -71.0589}
    bearing = location_calculations.get_bearing(new_york, boston)
    assert bearing > 45 and bearing < 60
