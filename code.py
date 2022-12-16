
print('dude')

import time

import board
import digitalio
import neopixel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet


NUM_PIXELS = 24
ENGINE_CORE = 12

COLOR_OFF = (0,0,0)

pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Effect Button
button_0 = digitalio.DigitalInOut(board.GP17)
button_0.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_0 = 0

# Speed Button
button_1 = digitalio.DigitalInOut(board.GP20)
button_1.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_1 = 1

DEBUG = True

class EffectDoNothing():
    def __init__(self):
        pass
    def animate(self):
        pixels.fill((0,0,0))
        if DEBUG:
            pixels[2] = (0,100,0)
        pixels.show()
def effect_nothing_gen():
    def effect_nothing():
        e = EffectDoNothing()
        return e
    return effect_nothing

def effect_rainbow_gen(speed):
    def rainbow():
        e = RainbowComet(pixels, speed=speed, reverse = True)
        return e
    return rainbow

def effect_bouncing_comet_gen(speed):
    def bouncing_comet():
        e = Comet(pixels, speed, (255,255,0), bounce=True)
        return e
    return bouncing_comet

EFFECTS = [
    [effect_nothing_gen()],
    [effect_rainbow_gen(0.25), effect_rainbow_gen(0.5), effect_rainbow_gen(0.1)],
    [effect_bouncing_comet_gen(0.25), effect_bouncing_comet_gen(0.1)]
]
EFFECTS_SIZE = len(EFFECTS)

# hard coding initial
current_effect_index = 1
current_speed_index = 0
current_effect = EFFECTS[current_effect_index][current_speed_index]()



print("HI")

changed = False

while True:
    # print("WOW")
    current_effect.animate()
    if button_0.value:
        current_effect_index = (current_effect_index + 1) % EFFECTS_SIZE
        current_speed_index = 0
        print("Changing effect")
        changed = True
    if button_1.value:
        current_speed_index = (current_speed_index + 1) % len(EFFECTS[current_effect_index])
        print("Changing speed to " + str(current_speed_index))
        changed = True
    if changed:
        current_effect = EFFECTS[current_effect_index][current_speed_index]()
        pixels.fill(COLOR_OFF)
        pixels.show()
        changed = False
    time.sleep(0.1)