from machine import Pin
import time

class Motor():
    def __init__(self, left_pin=22, right_pin=23):
        self.left = Pin(left_pin, Pin.OUT)
        self.right = Pin(right_pin, Pin.OUT)
    
    def rotate_clockwise(self):
        self.right.value(1)
        self.left.value(0)
    
    def rotate_counterclockwise(self):
        self.left.value(1)
        self.right.value(0)
    
    def stop(self):
        self.left.value(0)
        self.right.value(0)



if __name__ == '__main__':
    left = Pin(22, Pin.OUT)
    right = Pin(23, Pin.OUT)

    while True:
        left.value(1)
        right.value(0)
        time.sleep(1)
        left.value(0)
        right.value(1)
        time.sleep(1)