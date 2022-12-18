import time
from collections import OrderedDict, namedtuple

try:
    from typing import Any, Tuple
except ImportError:
    pass #meh
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from neopixel import NeoPixel

DEBUG = False
COLOR_OFF = (0,0,0)


class EffectEntry(object):
    def __init__ (self, effect):
        self.effect = effect
        self.name: str = ""
        self.speed: str = ""
        self.index_effect: int = 0
        self.index_speed: int = 0

    def full_name(self):
        if not self.speed:
            return self.name
        return "%s_%s" % (self.name, self.speed)
    def __repr__(self) -> str:
        return self.full_name()
NOT_FOUND_EFFECT = EffectEntry(None)


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

def effect_bouncing_comet_gen(pixels: NeoPixel, speed, color: Tuple):
    def bouncing_comet():
        e = Comet(pixels, speed, color, bounce=True)
        return e
    return bouncing_comet

class EffectWarpEnterpriseD():
    def __init__(self, pixels: NeoPixel, core:int, speed, top_dim, top_bright, bottom_dim, bottom_bright):
        # Parameters
        self.pixels = pixels
        self.core = core
        self.speed = speed
        self.top_dim = top_dim
        self.top_bright = top_bright
        self.bottom_dim = bottom_dim
        self.bottom_bright = bottom_bright

        # Starting conditions
        self.start_top = self.pixels.n - 1
        # TODO: Something going on here with pixel 0 being left out
        self.start_bottom = -1 * (self.pixels.n - self.core - self.core - 1)
        self.below_steps = abs(self.start_bottom) + 3

        # Iteration
        self.new_top = self.start_top
        self.new_bottom = self.start_bottom
        self.last_top = self.new_top
        self.last_bottom = self.new_bottom
        self.reset_pixels = []
    def animate(self):
        while self.reset_pixels:
            self.pixels[self.reset_pixels.pop()] = COLOR_OFF

        if self.last_bottom > -1:
            self.pixels[self.last_bottom] = self.bottom_dim
            self.reset_pixels.append(self.last_bottom)
        if self.new_bottom < 0:
            adjust = (self.below_steps - abs(self.new_bottom)) / self.below_steps
            self.pixels[0] = tuple([_ * adjust for _ in self.bottom_bright])
        if self.new_bottom > -1:
            self.pixels[self.new_bottom] = self.bottom_bright
            self.reset_pixels.append(self.new_bottom)
        self.pixels[self.last_top] = self.top_dim
        self.pixels[self.new_top] = self.top_bright
        self.reset_pixels.append(self.last_top)
        self.reset_pixels.append(self.new_top)
        self.pixels.show()

        self.last_top = self.new_top
        self.last_bottom = self.new_bottom
        self.new_top -= 1
        self.new_bottom += 1

        if self.new_top < self.core:
            self.new_top = self.start_top
        if self.new_bottom > self.core:
            self.new_bottom = self.start_bottom
        time.sleep(self.speed)
def effect_warp_loop_entd_gen(pixels: NeoPixel, core: int, speed, top_dim, top_bright, bottom_dim, bottom_bright):
    def warp_loop():
        e = EffectWarpEnterpriseD(pixels, core, speed, top_dim, top_bright, bottom_dim, bottom_bright)
        return e
    return warp_loop
def effect_warp_loop_entd_gen_speeds(pixels: NeoPixel, core:int, speeds: list, top_dim, top_bright, bottom_dim, bottom_bright):
    items = []
    for speed in speeds:
        items.append((str(speed), EffectEntry(effect_warp_loop_entd_gen(pixels, core, speed, top_dim, top_bright, bottom_dim, bottom_bright))))
    return items

def get_all_effect_entries(pixels: NeoPixel, core: int) -> Tuple[dict[str,dict[str,EffectEntry]],list[list[EffectEntry]]]:
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
        ("cometbounce_purple", OrderedDict([
            ("0.25", EffectEntry(effect_bouncing_comet_gen(pixels,0.25, (100,0,100)))),
            ("0.1", EffectEntry(effect_bouncing_comet_gen(pixels,0.1, (100,0,100))))
        ])),
        ("warpcore_blue", OrderedDict(
            effect_warp_loop_entd_gen_speeds(pixels, 12, [0.5, 0.25, 0.05],
                (0,0,40), (0,0,255), (0,0,40), (0,0,255))
        )),
        ("warpcore_purple", OrderedDict(
            effect_warp_loop_entd_gen_speeds(pixels, 12, [0.5, 0.25, 0.05],
                (40,0,40), (200,0,200), (40,0,40), (200,0,200))
        )),
        ("warpcore_xmas", OrderedDict(
            effect_warp_loop_entd_gen_speeds(pixels, 12, [0.5,0.25,0.05],
                (40,0,0), (255,0,0), (0,40,0), (0,255,0))
        ))
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
