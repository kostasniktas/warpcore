import time
import board
import neopixel
import digitalio

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 16

pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP17)
button.switch_to_input(pull=digitalio.Pull.DOWN)



ALL_COLORS = [
    ((0,0,255), (0,0,40)),
    ((255,0,0), (40,0,0))
]
BRIGHT = 0
DIM = 1
COLOR_INDEX = 0
COLOR = ALL_COLORS[COLOR_INDEX]

ENGINE_CORE = 6

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
        pixels[reset_pixels.pop()] = (0,0,0)

    if button.value:
        COLOR_INDEX = (COLOR_INDEX + 1) % len(ALL_COLORS)
        COLOR = ALL_COLORS[COLOR_INDEX]
    else:
        pixels[4] = (0,0,0)

    if last_bottom > -1:
        pixels[last_bottom] = COLOR[DIM]
        reset_pixels.append(last_bottom)
    if new_bottom < 0:
        adjust = (BELOW_STEPS - abs(new_bottom)) / BELOW_STEPS
        pixels[0] = (COLOR[BRIGHT][0] * adjust, COLOR[BRIGHT][1] * adjust, COLOR[BRIGHT][2] * adjust)
    if new_bottom > -1:
        pixels[new_bottom] = COLOR[BRIGHT]
        reset_pixels.append(new_bottom)
    pixels[last_top] = COLOR[DIM]
    pixels[new_top] = COLOR[BRIGHT]
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
