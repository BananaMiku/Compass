## Set Up
- ==Note: Only do this on a fresh ESP32 board!==
- Place ESP32 on breakout board with external ports facing the same direction, and connect to power via ESP32
- Run `pip install esptool`, verify installation with `esptool -h`
- Download the latest [firmware](https://micropython.org/download/ESP32_GENERIC/) for the ESP32 board (default WROOM board)
- Run `esptool erase_flash`
- Run `esptool --baud 460800 write_flash 0x1000 ESP32_BOARD_NAME-DATE-VERSION.bin`
    - Replace *ESP32_BOARD_NAME-DATE-VERSION.bin* with the appropriate *.bin* file downloaded previously
    - This will flash the firmware onto ESP32
- Further debugging help can be found [here](https://micropython.org/download/ESP32_GENERIC/)
- `esptool` documentation found [here](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/index.html)

## Running Program
- Run `pip install mpremote`
- Run `mpremote devs` to locate ESP32
    - On MacOS, the port for ESP32 might look something like this: `/dev/cu.usbserial-0001`
- To verify connection to ESP32, run `mpremote connect /dev/cu.usbserial-0001 exec "print('hello from esp32')"`
    - Replace */dev/cu.usbserial-0001* with the appropriate port
#### Dependecies
- The program needs the following drivers, downloadable via:
    - BNO055 IMU: `mpremote mip install github:micropython-IMU/micropython-bno055`
    - Adafruit Ultimate GPS: `mpremote connect /dev/cu.usbserial-0001 mip install https://raw.githubusercontent.com/inmcm/micropyGPS/master/micropyGPS.py`
        - Replace */dev/cu.usbserial-0001* with the appropriate port
#### Script
- This script will automatically:
    - Remove old MicroPython files from ESP32
    - Move new MicroPython files to ESP32
    - Run the repo through `main.py`
- First, make it an executable with `chmod +x flash.sh`
- Then, run the script `./flash.sh /dev/cu.usbserial-0001`
    - Be sure to change the port appropriately
- Or, run a program as a three step process:
    1. Upload as `mpremote connect /dev/cu.usbserial-0001 fs cp main.py :main.py`
        - *main.py* is entry point for MicroPython
        - Replace */dev/cu.usbserial-0001* with the appropriate port
    2. Reset as `mpremote connect /dev/cu.usbserial-0001 reset`
    3. Watch as `mpremote connect /dev/cu.usbserial-0001 repl`
#### Exiting Program
- ctrl + \] or ctrl + x to exit mpremote shell
- Hard remove the file on ESP3 with `mpremote connect /dev/cu.usbserial-0001 fs rm :main.py`