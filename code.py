import time

import board
import digitalio
import neopixel

import effects

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

EFFECTS, EFFECTS_ITERATIONS = effects.get_all_effect_entries(pixels)
EFFECTS_SIZE = len(EFFECTS_ITERATIONS)

print("All the supported effects: " + str([item for sublist in EFFECTS_ITERATIONS for item in sublist]))

def get_by_name(effect_name: str) -> effects.EffectEntry:
    name, speed = effect_name.rsplit("_", 1)
    try:
        effect_entry = EFFECTS[name][speed]
        return effect_entry
    except:
        return effects.NOT_FOUND_EFFECT

def get_by_index(effect: int, speed: int) -> effects.EffectEntry:
    try:
        effect_entry = EFFECTS_ITERATIONS[effect][speed]
        return effect_entry
    except:
        return effects.NOT_FOUND_EFFECT


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
