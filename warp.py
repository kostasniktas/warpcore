
from typing import List, Tuple
import time
import subprocess

NUM_PIXELS = 16

# Assume middle is right in the middle or in the bottom half
MIDDLE = 6 # location of core
# BOTTOM_SHORTER = (NUM_PIXELS / 2) >= MIDDLE
BOTTOM_SHORTER = True


def get_pixels() -> List[Tuple[int,int,int]]:
    pixels = []
    for _ in range(NUM_PIXELS):
        pixels.append((0,0,0))
    return pixels

def print_pixels(pixels: List[Tuple[int,int,int]]) -> None:
    print("======TOP======")
    for i in range(NUM_PIXELS-1,-1,-1):
        if i == MIDDLE:
            print(f"{str(pixels[i])} MIDDLE")
        else:
            print(str(pixels[i]))
    print("====BOTTOM====")

def warp_pixels() -> None:
    pixels = get_pixels()
    last_top = NUM_PIXELS
    last_bottom = -1
    diff = NUM_PIXELS - MIDDLE + 1
    # print(diff)
    # print(NUM_PIXELS - MIDDLE + 1)
    # sys.exit(0)
    while True:
        new_bottom = last_bottom + 1
        new_top = last_top - 1

        # Resetting
        # assumes core at middle or lower
        if new_bottom > MIDDLE:
            new_bottom = 0
        if new_top <= MIDDLE:
            new_top = NUM_PIXELS - 1

        # Colors
        # pixels = get_pixels()
        pixels[new_top] = (0,0,255)
        pixels[new_bottom] = (0,0,255)
        if last_bottom > -1:
            pixels[last_bottom] = (0,0,40)
        if last_top < NUM_PIXELS:
            pixels[last_top] = (0,0,40)

        # View
        subprocess.call("clear")
        print_pixels(pixels)

        try:
            pixels[new_top] = (0,0,0)
            pixels[new_bottom] = (0,0,0)
            pixels[last_top] = (0,0,0)
            pixels[last_bottom] = (0,0,0)
        except IndexError:
            pass

        last_top = new_top
        last_bottom = new_bottom
        time.sleep(1)



def main():
    print("i'm main")
    subprocess.call("clear")
    warp_pixels()
    # print_pixels(get_pixels())

if __name__ == "__main__":
    main()