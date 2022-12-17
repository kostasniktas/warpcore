
print('dude')

import time
import wifi
from collections import OrderedDict, namedtuple

try:
    from typing import Any
except ImportError:
    pass #meh

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

class EffectEntry(object):
    def __init__ (self, effect):
        self.effect = effect
        self.name: str = ""
        self.speed: str = ""
        self.index_effect: int = 0
        self.index_speed: int = 0

    def full_name(self):
        return "%s_%s" % (self.name, self.speed)
    def __repr__(self) -> str:
        return self.full_name()

EffectCoordinate = namedtuple("EffectCoordinate", ("effect", "index_effect", "index_speed", "effect_keys"))
NOT_FOUND_EFFECT = EffectEntry(None)

# Allows for finding things by keys
EFFECTS: dict[str, dict[str, Any]] = OrderedDict([
    ("nothing", OrderedDict([
        ("", EffectEntry(effect_nothing_gen()))
    ])),
    ("rainbow", OrderedDict([
        ("0.25", EffectEntry(effect_rainbow_gen(0.25))),
        ("0.5", EffectEntry(effect_rainbow_gen(0.5))),
        ("0.1", EffectEntry(effect_rainbow_gen(0.1)))
    ])),
    ("comet", OrderedDict([
        ("0.25", EffectEntry(effect_bouncing_comet_gen(0.25))),
        ("0.1", EffectEntry(effect_bouncing_comet_gen(0.1)))
    ]))
])

# Allows to iterate
EFFECTS_ITERATIONS = []
i = 0
for effect in EFFECTS.keys():
    j = 0
    all_speeds = []
    for speed in EFFECTS[effect].keys():
        effect_entry: EffectEntry = EFFECTS[effect][speed]
        effect_entry.index_effect = i
        effect_entry.index_speed = j
        effect_entry.name = effect
        effect_entry.speed = speed
        all_speeds.append(effect_entry)
        j+=1
    i+=1
    EFFECTS_ITERATIONS.append(all_speeds)
EFFECTS_SIZE = len(EFFECTS_ITERATIONS)
# print(EFFECTS_ITERATIONS)
# print(EFFECTS)

def get_by_name(effect_name: str) -> EffectEntry:
    name, speed = effect_name.rsplit("_", 1)
    try:
        effect_entry = EFFECTS[name][speed]
        return effect_entry
    except:
        return NOT_FOUND_EFFECT

def get_by_index(effect: int, speed: int) -> EffectEntry:
    try:
        effect_entry = EFFECTS_ITERATIONS[effect][speed]
        return effect_entry
    except:
        return NOT_FOUND_EFFECT


# hard coding initial
current_entry = get_by_name("comet_0.1")
current_effect_index = current_entry.index_effect
current_speed_index = current_entry.index_speed
current_effect = current_entry.effect()

print("HI")

changed = False

while True:
    current_effect.animate()
    if button_0.value:
        current_effect_index = (current_effect_index + 1) % EFFECTS_SIZE
        current_speed_index = 0
        print("Changing effect")
        changed = True
    if button_1.value:
        current_speed_index = (current_speed_index + 1) % len(EFFECTS_ITERATIONS[current_effect_index])
        print("Changing speed to " + str(current_speed_index))
        changed = True
    if changed:
        effect_entry = get_by_index(current_effect_index,current_speed_index)
        pixels.fill(COLOR_OFF)
        pixels.show()
        changed = False
        print("Changing to " + effect_entry.full_name())
        current_effect = effect_entry.effect()
    time.sleep(0.1)
