import gps
import config
import barfindr
import location_calculations as lc
import local_orientation as lo

def main():
    last_scan = None 
    bars = []
    while True:
        cur_location = gps.get_gps_location()
        if cur_location == None:
            continue
        if last_scan == None or lc.get_distance(cur_location, last_scan) > config.RESCAN_DIST:
            last_scan = cur_location
            bars = barfindr.get_bars(cur_location, 10000)
        closest_bar = barfindr.find_closest_bar(bars, cur_location)
        angle = lc.get_bearing(closest_bar, cur_location)
        
                
        # gets current orientation in terms of direction and degree
        curr_dir, bearing = lo.get_direction()

main()