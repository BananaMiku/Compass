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
    cur_location = {}
    bars = []

    while True:
        # Read GPS UART data
        # local.gps_update()
        lat, lon = local.gps_get_position()

        if lat and lon:
            cur_location['lat'], cur_location['lng'] = lat, lon

        if len(cur_location) < 2:
            motor.stop()
            continue
            #just continue moving the motor to the last acc cur location if we can 
        if last_scan is None or lc.get_distance(cur_location, last_scan) > RESCAN_DIST:
            last_scan = cur_location
            bars = barfindr.get_bars(cur_location, 10000)
        closest_bar = barfindr.find_closest_bar(bars, cur_location)
        if closest_bar is None:
            motor.stop()
            continue
        bar_coords = barfindr.extract_lat_lng(closest_bar)

        # Get current heading from IMU
        _, heading = local.imu_get_direction()

        # Calculate angle offset to closest bar (-180 to 180)
        offset = pa.degree_offset(lat, lon, bar_coords['lat'], bar_coords['lng'], heading)
        print(f"offset: {offset}")

        # Drive needle to offset angle using encoder feedback
        motor.go_to_angle(offset)

def main_calibration():
    local = Locality()
    motor = Motor()  # L298N: ENA=25, IN1=26, IN2=27 | Encoder: A=32, B=33
    last_scan = None
    cur_location = {}
    cur_speed = 300
    last_update = time.ticks_ms()
    bars = []

    while True:
        # Read GPS UART data
        # local.gps_update()
        if(time.ticks_diff(now, last_update) / 1000.0 > 10):
            cur_speed += 10
            last_update = time.ticks_ms()
                
        lat, lon = local.gps_get_position()

        if lat and lon:
            cur_location['lat'], cur_location['lng'] = lat, lon

        if len(cur_location) < 2:
            motor.stop()
            continue
            #just continue moving the motor to the last acc cur location if we can 
        if last_scan is None or lc.get_distance(cur_location, last_scan) > RESCAN_DIST:
            last_scan = cur_location
            bars = barfindr.get_bars(cur_location, 10000)
        closest_bar = barfindr.find_closest_bar(bars, cur_location)
        if closest_bar is None:
            motor.stop()
            continue
        bar_coords = barfindr.extract_lat_lng(closest_bar)

        # Get current heading from IMU
        _, heading = local.imu_get_direction()

        # Calculate angle offset to closest bar (-180 to 180)
        offset = pa.degree_offset(lat, lon, bar_coords['lat'], bar_coords['lng'], heading)
        print(f"offset: {offset}")

        # Drive needle to offset angle using encoder feedback
        motor.go_to_angle_calibration(offset, cur_speed)


main_calibration()
