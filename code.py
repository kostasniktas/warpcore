import time
import board
import neopixel
import digitalio

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 16
ENGINE_CORE = 6

COLOR_OFF = (0,0,0)



pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP17)
button.switch_to_input(pull=digitalio.Pull.DOWN)



def do_nothing_gen():
    def do_nothing():
        pixels[0] = (50,0,0)
        pixels[0] = COLOR_OFF
        while True:
            if button.value:
                pixels[2] = COLOR_OFF
                return
            pixels[2] = (0,10,0)
            time.sleep(0.25)
    return lambda: do_nothing()

def warp_loop_gen(dim, bright):
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
                return

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

EFFECTS = [
    warp_loop_gen((0,0,40), (0,0,255)),
    warp_loop_gen((40,0,0), (255,0,0)),

    do_nothing_gen()
]
EFFECT_SIZE = len(EFFECTS)

effect_index = 0
while True:
    EFFECTS[effect_index]()
    effect_index = (effect_index + 1) % EFFECT_SIZE
    time.sleep(1)
