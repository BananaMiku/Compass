import config
import barfindr
import location_calculations as lc
from local_orientation import Locality
from motor_test import Motor
import position_adjustment as pa
import time

DEADZONE = 10  # degrees tolerance before stopping motor
RESCAN_DIST = 100  # meters before re-fetching bars

def main():
    local = Locality()
    motor = Motor(left_pin=25, right_pin=26)  # IMU uses pin (22, 21)
    last_scan = None
    bars = []
    # while True:
    #     print(local.imu_get_direction())

    while True:
        # Read GPS UART data
        # local.gps_update()
        lat, lon = local.gps_get_position()

        if lat is None or lon is None:
            motor.stop()
            time.sleep(0.1)
            continue

        cur_location = {'lat': lat, 'lng': lon}
        if last_scan is None or lc.get_distance(cur_location, last_scan) > RESCAN_DIST:
            last_scan = cur_location
            bars = barfindr.get_bars(cur_location, 10000)
        closest_bar = barfindr.find_closest_bar(bars, cur_location)
        if closest_bar is None:
            motor.stop()
            time.sleep(0.5)
            continue
        bar_coords = barfindr.extract_lat_lng(closest_bar)

        # Get current heading from IMU
        _, heading = local.imu_get_direction()
        print(heading)

        # Calculate angle offset to closest bar
        offset = pa.degree_offset(lat, lon, bar_coords['lat'], bar_coords['lng'], heading)

        # Drive motor toward target
        if abs(offset) < DEADZONE:
            motor.stop()
        elif offset > 0:
            motor.rotate_clockwise()
        else:
            motor.rotate_counterclockwise()

        time.sleep(0.1)

main()