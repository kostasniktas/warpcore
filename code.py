import time

import board
import digitalio
import neopixel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet

NUM_PIXELS = 24
ENGINE_CORE = 12

COLOR_OFF = (0,0,0)

# TODO: Figure out how to get vscode to see afafruit libraries beyond neopixel


pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button_0 = digitalio.DigitalInOut(board.GP17)
button_0.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_0 = 0

button_1 = digitalio.DigitalInOut(board.GP20)
button_1.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_1 = 1

DEBUG = True

#
# Do nothing
#
def do_nothing_gen():
    def do_nothing(speed):
        pixels[0] = (50,0,0)
        pixels[0] = COLOR_OFF
        while True:
            if button_0.value:
                pixels[2] = COLOR_OFF
                return BUTTON_0
            if button_1.value:
                pixels[2] = COLOR_OFF
                return BUTTON_1
            if DEBUG:
                pixels[2] = (0,10,0)
            time.sleep(speed)
    return do_nothing

#
# Simulate Enterprise D engine core pulses
#
def warp_loop_gen_enterprise_d(dim, bright):
    def warp_loop(speed):
        START_TOP = NUM_PIXELS - 1
        START_BOTTOM = -1 * (NUM_PIXELS - ENGINE_CORE - ENGINE_CORE - 1)
        BELOW_STEPS = abs(START_BOTTOM) + 3

        new_top = START_TOP
        new_bottom = START_BOTTOM
        last_top = new_top
        last_bottom = new_bottom

        reset_pixels = []
        while True:
            while reset_pixels:
                pixels[reset_pixels.pop()] = COLOR_OFF

            if button_0.value:
                return BUTTON_0
            if button_1.value:
                return BUTTON_1

            if last_bottom > -1:
                pixels[last_bottom] = dim
                reset_pixels.append(last_bottom)
            if new_bottom < 0:
                adjust = (BELOW_STEPS - abs(new_bottom)) / BELOW_STEPS
                pixels[0] = (bright[0] * adjust, bright[1] * adjust, bright[2] * adjust)
            if new_bottom > -1:
                pixels[new_bottom] = bright
                reset_pixels.append(new_bottom)
            pixels[last_top] = dim
            pixels[new_top] = bright
            reset_pixels.append(last_top)
            reset_pixels.append(new_top)


            pixels.show()


            last_top = new_top
            last_bottom = new_bottom
            new_top -= 1
            new_bottom += 1

            if new_top < ENGINE_CORE:
                new_top = START_TOP
            if new_bottom > ENGINE_CORE:
                new_bottom = START_BOTTOM

            time.sleep(speed)
    return warp_loop


#
# Rainbow effect
#
def rainbow_gen():
    def rainbow(speed):
        rainbow_effect = RainbowComet(pixels, speed=speed, reverse=True)
        while True:
            if button_0.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return BUTTON_0
            if button_1.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return BUTTON_1
            rainbow_effect.animate()
    return rainbow


#
# Go Down and Go Up
#
def bouncing_comet_gen(colors):
    def bouncing_commet(speed):
        commet = Comet(pixels, speed, colors, bounce=True)
        while True:
            if button_0.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return BUTTON_0
            if button_1.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return BUTTON_1
            commet.animate()
    return bouncing_commet

EFFECTS = [
    warp_loop_gen_enterprise_d((0,0,40), (0,0,255)),
    warp_loop_gen_enterprise_d((40,0,40), (200,0,200)),
    bouncing_comet_gen((100,0,100)),
    rainbow_gen(),


    do_nothing_gen()
]
EFFECT_SIZE = len(EFFECTS)

SPEEDS = [0.25, 0.5, 1, 0.01, 0.05, 0.1]
SPEEDS_SIZE = len(SPEEDS)

effect_index = 0
speed_index = 0
while True:
    ret = EFFECTS[effect_index](SPEEDS[speed_index])
    if ret == BUTTON_0:
        effect_index = (effect_index + 1) % EFFECT_SIZE
        speed_index = 0
    if ret == BUTTON_1:
        speed_index = (speed_index + 1) % SPEEDS_SIZE
    time.sleep(0.25)
