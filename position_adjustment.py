import math

def degree_offset(curr_lat, curr_lon, target_lat, target_lon, heading):
    # Convert latitude and longitude to radians
    curr_lat = curr_lat * math.pi / 180
    curr_lon = curr_lon * math.pi /180
    target_lat = target_lat * math.pi / 180
    target_lon = target_lon * math.pi / 180
    
    delta_lon = target_lon - curr_lon
    
    east_west_comp = math.sin(delta_lon) * math.cos(target_lat)
    north_south_comp = math.cos(curr_lat) * math.sin(target_lat) - math.sin(curr_lat) * math.cos(target_lat) * math.cos(delta_lon)
    
    theta = math.atan2(east_west_comp, north_south_comp)
    
    bearing = theta * (180 / math.pi)
    
    bearning_norm = (bearing + 360) % 360
    
    offset = bearning_norm - heading
    
    # Normalize to -180 to 180
    offset_norm = ((offset + 180) % 360) - 180
    
    return offset_norm