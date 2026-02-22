from machine import Pin, SoftI2C, UART
from bno055 import BNO055
from micropyGPS import MicropyGPS
import time

class Locality:
    def __init__(self, 
                # IMU pins (BNO055)
                scl=22, sda=21, freq=100000, addr=0x28, local_declination=-14.0,
                # GPS UART (Adafruit Ultimate GPS)
                gps_uart_id=2, gps_baud=9600, gps_tx=17, gps_rx=16
                ):
        # IMU
        # BNO055 boot time
        time.sleep_ms(600)
        
        self.i2c = SoftI2C(
            scl=Pin(scl),
            sda=Pin(sda),
            freq=freq,
            timeout=100000  # BNO055 clock stretching
        )

        self.imu = BNO055(self.i2c, address=addr)
        self.local_declination = float(local_declination)
        
        # GPS
        self.gps = MicropyGPS()
        self.uart = UART(
            gps_uart_id,
            baudrate=gps_baud,
            tx=Pin(gps_tx),
            rx=Pin(gps_rx),
        )
        self._last_print = time.ticks_ms()


    def set_local_declination(self, local_declination=0.0):
        """Local declination vaires based on geographical location to the magnetic north pole.
        Ex: Boston has -14 degrees due west and Sydney has +13 degrees due east.
        """
        self.local_declination = float(local_declination)

    def imu_get_direction(self):
        """Returns direction in text and number. Good to call sleep() before invoking this function in a repeated loop.

        Args:
            None

        Returns:
            curr_dir: current direction in 8-direction format
            bearing: degrees of compass bearing
        """
        directions = [
            "North", "Northeast",
            "East", "Southeast",
            "South", "Southwest",
            "West", "Northwest"
        ]
        # yaw is 0 to 360
        yaw = self.imu.euler()[0]
        bearing = (yaw + self.local_declination) % 360
        
        # BNO055 calibrated at 0 degrees as North
        # +- 22.5 to center to North at 0
        direction_idx = int(((bearing + 22.5) // 45) % 8)
        curr_dir = directions[direction_idx]
        
        return curr_dir, bearing

    def gps_update(self):
        """Reads UART bytes and feeds them into MicropyGPS for processing.
        Physical GPS as NMEA Bytes -> ESP32 via UART -> MicroGPS Library -> Parse -> Update Location Data
        """
        if self.uart.any():
            data = self.uart.read()
            if data:
                for b in data:
                    self.gps.update(chr(b))
    
    def gps_has_fix(self):
        """Returns bool for whether GPS has fix on satellite.
        """
        return bool(getattr(self.gps, "valid", False))
    
    def gps_get_position(self):
        """Returns lat. and lon. of current location.
        Ex. return vals: [42, 23.7427, 'N']   [72, 31.8539, 'W']
        """
        if self.gps_has_fix():
            return self.gps.latitude, self.gps.longitude
        else:
            return None, None