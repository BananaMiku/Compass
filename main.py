import config
import barfindr
import location_calculations as lc
from local_orientation import Locality
from motor_test import Motor
import position_adjustment as pa
import time

RESCAN_DIST = 100  # meters before re-fetching bars

def main():
    local = Locality()
    motor = Motor()  # L298N: ENA=25, IN1=26, IN2=27 | Encoder: A=32, B=33
    last_scan = None
    bars = []

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

        # Calculate angle offset to closest bar (-180 to 180)
        offset = pa.degree_offset(lat, lon, bar_coords['lat'], bar_coords['lng'], heading)
        print(f"offset: {offset}")

        # Drive needle to offset angle using encoder feedback
        motor.go_to_angle(offset)

        time.sleep_ms(50)

main()