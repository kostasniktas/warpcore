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


# TODO: Let the bottom one be on softer until more

ENGINE_CORE = 7

START_TOP = NUM_PIXELS - 1
START_BOTTOM = -1 * (NUM_PIXELS - ENGINE_CORE - ENGINE_CORE - 1)

new_top = START_TOP
new_bottom = START_BOTTOM
last_top = new_top
last_bottom = new_bottom

reset_pixels = []
while True:
    while reset_pixels:
        pixels[reset_pixels.pop()] = (0,0,0)

    if last_bottom > -1:
        pixels[last_bottom] = (0,0,40)
        reset_pixels.append(last_bottom)
    if new_bottom > -1:
        pixels[new_bottom] = (0,0,255)
        reset_pixels.append(new_bottom)
    pixels[last_top] = (0,0,40)
    pixels[new_top] = (0,0,255)
    reset_pixels.append(last_top)
    reset_pixels.append(new_top)

    pixels.show()

    # if last_bottom > -1:
    #     pixels[last_bottom] = (0,0,0)
    # if new_bottom > -1:
    #     pixels[new_bottom] = (0,0,0)
    # pixels[last_top] = (0,0,0)
    # pixels[new_top] = (0,0,0)

    last_top = new_top
    last_bottom = new_bottom
    new_top -= 1
    new_bottom += 1

    if new_top < ENGINE_CORE:
        new_top = START_TOP
    if new_bottom > ENGINE_CORE:
        new_bottom = START_BOTTOM
    
    time.sleep(0.25)
