# Write your code here :-)
from microbit import *

pixel_x = 2
pixel_y = 2
brightness = 1
sensitivity = 40
speed = 100

while True:
    sleep(speed)
    display.clear()
    display.set_pixel(pixel_x, pixel_y, brightness)
    x_reading = accelerometer.get_x()
    y_reading = accelerometer.get_y()
    if x_reading < -sensitivity:
        pixel_x = max(0, pixel_x -1)
    elif x_reading > sensitivity:
        pixel_x = min(4, pixel_x + 1)
    if y_reading < -sensitivity:
        pixel_y = max(0, pixel_y - 1)
    elif y_reading > sensitivity:
        pixel_y = min(4, pixel_y + 1)
    brightness += 1
    if brightness == 10:
        brightness = 1
