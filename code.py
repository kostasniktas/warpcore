# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red, green, and blue in sequence.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import time
import board
import neopixel
import digitalio

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 16

pixels = neopixel.NeoPixel(board.GP16, num_pixels)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    pixels.fill((255, 0, 0))
    time.sleep(0.25)
    pixels.fill((0, 255, 0))
    time.sleep(0.25)
    pixels.fill((0, 0, 255))
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)