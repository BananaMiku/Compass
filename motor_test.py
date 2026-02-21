from machine import Pin
import time

left = Pin(22, Pin.OUT)
right = Pin(23, Pin.OUT)

while True:
    left.value(1)
    right.value(0)
    time.sleep(1)
    left.value(0)
    right.value(1)
    time.sleep(1)