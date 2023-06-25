# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# Utilized CircuitPython Essentials NeoPixel example

import time
import board
from rainbowio import colorwheel
import neopixel
import pwmio
import digitalio

print(dir(board))


switch = digitalio.DigitalInOut(board.D1)  # For Circuit Playground Express
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
old_value = switch.value

pwm = None

pixel_pin = board.NEOPIXEL
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)



def rainbow_cycle(wait):
    global old_value
    global pwm
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()

        if not (switch.value == old_value):
            if not switch.value:
                print("Turning On")
                pwm = pwmio.PWMOut(board.D0, duty_cycle=int(0.95*(2**16)), frequency=420)

            else:
                print("Turning Off")
                pwm.deinit()

            old_value = switch.value
        time.sleep(wait)


while True:

    rainbow_cycle(0.05)  # Increase the number to slow down the rainbow
