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

target_voltage = 3.1

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

# calculate what percentage time to leave the battery on
# use square to get equal power
def get_period(v_battery, v_goal):
    p_goal = v_goal * v_goal
    p_actual = v_battery * v_battery
    return min(p_goal / p_actual, 1.0)

pwm = pwmio.PWMOut(board.D0, duty_cycle=0, frequency=420)

def adjust_pwm(period):
    global pwm
    # you can't give >100%
    duty_cycle = min(int(period*(2**16)), 2**16-1)
    # print("period:", period, "duty cycle:", duty_cycle)
    pwm.duty_cycle = duty_cycle


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
            print("Battery Voltage:", "{:.3f}".format(b_voltage))
            old_b_voltage = b_voltage
            # If we are on, adjust the pwm too
            if not switch.value:
                period = get_period(b_voltage, target_voltage)
                print("Adjusting duty cycle to ", "{:.2f}".format(period*100), "%")
                adjust_pwm(period)

        if not (switch.value == old_value):
            if not switch.value:
                print("Turning On")
                adjust_pwm(get_period(b_voltage, target_voltage))

            else:
                print("Turning Off")
                adjust_pwm(0.0)

            old_value = switch.value
        time.sleep(wait)


while True:

    rainbow_cycle(0.05)  # Increase the number to slow down the rainbow
