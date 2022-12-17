from collections import OrderedDict, namedtuple

try:
    from typing import Any, Tuple
except ImportError:
    pass #meh
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from neopixel import NeoPixel

DEBUG = True

class EffectDoNothing():
    def __init__(self, pixels: NeoPixel):
        self.pixels = pixels
    def animate(self):
        self.pixels.fill((0,0,0))
        if DEBUG:
            self.pixels[2] = (0,100,0)
        self.pixels.show()
def effect_nothing_gen(pixels: NeoPixel):
    def effect_nothing():
        e = EffectDoNothing(pixels)
        return e
    return effect_nothing

def effect_rainbow_gen(pixels: NeoPixel, speed):
    def rainbow():
        e = RainbowComet(pixels, speed=speed, reverse = True)
        return e
    return rainbow

def effect_bouncing_comet_gen(pixels: NeoPixel, speed):
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

NOT_FOUND_EFFECT = EffectEntry(None)

def get_all_effect_entries(pixels: NeoPixel) -> Tuple[dict[str,dict[str,EffectEntry]],list[list[EffectEntry]]]:
    print("Build effects from a module")
    # Allows for finding things by keys
    EFFECTS: dict[str, dict[str, Any]] = OrderedDict([
        ("nothing", OrderedDict([
            ("", EffectEntry(effect_nothing_gen(pixels)))
        ])),
        ("rainbow", OrderedDict([
            ("0.25", EffectEntry(effect_rainbow_gen(pixels,0.25))),
            ("0.5", EffectEntry(effect_rainbow_gen(pixels,0.5))),
            ("0.1", EffectEntry(effect_rainbow_gen(pixels,0.1)))
        ])),
        ("comet", OrderedDict([
            ("0.25", EffectEntry(effect_bouncing_comet_gen(pixels,0.25))),
            ("0.1", EffectEntry(effect_bouncing_comet_gen(pixels,0.1)))
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

    return (EFFECTS, EFFECTS_ITERATIONS)
    # print(EFFECTS_ITERATIONS)
    # print(EFFECTS)
