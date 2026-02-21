## Set Up
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
- Run `mpremote connect /dev/cu.usbserial-0001 repl` to connect to ESP32
    - Replace */dev/cu.usbserial-0001* with the appropriate port
- Run the script `./flash.sh /dev/cu.usbserial-0001`
    - Be sure to change the port appropriately
- Or, run a program as a three step process:
    1. Upload as `mpremote connect /dev/cu.usbserial-0001 fs cp main.py :main.py`
        - *main.py* is entry point for MicroPython
        - Replace */dev/cu.usbserial-0001* with the appropriate port
    2. Reset as `mpremote connect /dev/cu.usbserial-0001 reset`
    3. Watch as `mpremote connect /dev/cu.usbserial-0001 repl`
- ctrl + \] or ctrl + x to exit mpremote shell
- Hard remove the file on ESP3 with `mpremote connect /dev/cu.usbserial-0001 fs rm :main.py`