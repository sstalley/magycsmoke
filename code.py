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
from analogio import AnalogIn

print(dir(board))


switch = digitalio.DigitalInOut(board.D1)  # For Circuit Playground Express
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
old_value = switch.value

pwm = None

pixel_pin = board.NEOPIXEL
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

analog_in = AnalogIn(board.A2)

def get_voltage(pin):
    rv1 = rv2 = 15000 # set these to the resistor values you chose
    vdiv = rv1 / (rv1 + rv2)
    return (pin.value * 3.3) / 65536 / vdiv

b_voltage = get_voltage(analog_in)

def rainbow_cycle(wait):
    global old_value
    global pwm
    global b_voltage
    old_b_voltage = b_voltage
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()

        b_voltage = get_voltage(analog_in)
        if not (b_voltage == old_b_voltage):
            print("Battery Voltage:", "{:.2f}".format(b_voltage))
            old_b_voltage = b_voltage

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
