import time

import board
import digitalio
import neopixel
from rainbowio import colorwheel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet



# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 16
ENGINE_CORE = 6

COLOR_OFF = (0,0,0)

# TODO: Figure out how to get vscode to see afafruit libraries beyond neopixel


pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP17)
button.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.GP20)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

DEBUG = True

#
# Do nothing
#
def do_nothing_gen():
    def do_nothing():
        pixels[0] = (50,0,0)
        pixels[0] = COLOR_OFF
        while True:
            if button.value:
                pixels[2] = COLOR_OFF
                return 0
            if button2.value:
                pixels[2] = COLOR_OFF
                return 1
            if DEBUG:
                pixels[2] = (0,10,0)
            time.sleep(0.25)
    return lambda: do_nothing()

#
# Simulate Enterprise D engine core pulses
#
def warp_loop_gen_enterprise_d(dim, bright):
    def warp_loop(dim, bright):
        START_TOP = NUM_PIXELS - 1
        START_BOTTOM = -1 * (NUM_PIXELS - ENGINE_CORE - ENGINE_CORE - 1)
        BELOW_STEPS = abs(START_BOTTOM) + 2

        new_top = START_TOP
        new_bottom = START_BOTTOM
        last_top = new_top
        last_bottom = new_bottom

        reset_pixels = []
        while True:
            while reset_pixels:
                pixels[reset_pixels.pop()] = COLOR_OFF

            if button.value:
                return 0
            if button2.value:
                return 1

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

            time.sleep(0.25)
    return lambda: warp_loop(dim, bright)


#
# Rainbow effect
#
def rainbow_gen(speed):
    def rainbow(speed):
        rainbow_effect = RainbowComet(pixels, speed=speed, reverse=True)
        while True:
            if button.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return 0
            if button2.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return 1
            rainbow_effect.animate()
    return lambda: rainbow(speed)


#
# Go Down and Go Up
#
def bouncing_comet_gen(colors, speed):
    def bouncing_commet(colors, speed):
        commet = Comet(pixels, speed, colors, bounce=True)
        while True:
            if button.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return 0
            if button2.value:
                pixels.fill(COLOR_OFF)
                pixels.show()
                return 1
            commet.animate()
    return lambda : bouncing_commet(colors, speed)

EFFECTS = [
    warp_loop_gen_enterprise_d((0,0,40), (0,0,255)),
    warp_loop_gen_enterprise_d((40,0,40), (200,0,200)),
    bouncing_comet_gen((100,0,100), 0.25),
    rainbow_gen(0.25),


    do_nothing_gen()
]
EFFECT_SIZE = len(EFFECTS)

effect_index = 0
while True:
    ret = EFFECTS[effect_index]()
    if ret == 0:
        effect_index = (effect_index + 1) % EFFECT_SIZE
    if ret == 1:
        effect_index = (effect_index - 1) % EFFECT_SIZE
    time.sleep(1)
