from machine import Pin, SoftI2C
from bno055 import BNO055
import time

# BNO055 boot time
time.sleep_ms(600)

i2c = SoftI2C(
    scl=Pin(22),
    sda=Pin(21),
    freq=100000,
    timeout=100000 #BNO055 clock stretching
)

imu = BNO055(i2c, address=0x28)
# BNO055 measures relative to magnetic north
# Define local declination for higer accuracy
local_declination = -14.0 

def get_direction():
    """Returns direction in text and number.

    Args:
        None

    Returns:
        curr_dir: current direction in 8-direction format
        bearing: degrees of compass bearing
    """
    time.sleep(0.2)
    directions = [
        "North",
        "Northeast",
        "East",
        "Southeast",
        "South",
        "Southwest",
        "West",
        "Northwest"
    ]
    # yaw is 0 to 360
    yaw = imu.euler()[0]
    bearing = (yaw + local_declination) % 360
    
    # BNO055 calibrated at 0 degrees as North
    # +- 22.5 to center to North at 0
    direction_idx = int(((bearing + 22.5) // 45) % 8)
    curr_dir = directions[direction_idx]
    
    # print(curr_dir, " ", bearing)
    return curr_dir, bearing