import gps
import config
import barfindr
import location_calculations as lc
from local_orientation import *
import time

def main():
    # Initialize IMU and GPS object
    local = Locality()
    last_scan = None 
    bars = []
    # TODO need intervaled reading from imu vs. gps
    while True:
        curr_dir, bearing = local.imu_get_direction()
        print(curr_dir, " ", bearing)
        local.gps_update()
        latitude, longitude = local.gps_get_position()
        print(latitude, " ", longitude)
        
        # cur_location = gps.get_gps_location()
        # if cur_location == None:
        #     continue
        # if last_scan == None or lc.get_distance(cur_location, last_scan) > config.RESCAN_DIST:
        #     last_scan = cur_location
        #     bars = barfindr.get_bars(cur_location, 10000)
        # closest_bar = barfindr.find_closest_bar(bars, cur_location)
        # angle = lc.get_bearing(closest_bar, cur_location)

main()