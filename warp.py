
from typing import List, Tuple
import time
import subprocess

NUM_PIXELS = 16

# Assume middle is right in the middle or in the bottom half
MIDDLE = 6 # location of core


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

    start_top = NUM_PIXELS - 1
    start_bottom = -1 * (NUM_PIXELS - MIDDLE - MIDDLE - 1)

    new_top = start_top
    new_bottom = start_bottom

    last_bottom = new_bottom
    last_top = new_top
    while True:
        if last_bottom > -1:
            pixels[last_bottom] = (0,0,40)
        if new_bottom > -1:
            pixels[new_bottom] = (0,0,255)
        
        pixels[last_top] = (0,0,40)
        pixels[new_top] = (0,0,255)

        subprocess.call("clear")
        print_pixels(pixels)
        print((last_top, last_bottom))
        print((new_top, new_bottom))

        pixels[last_top] = (0,0,0)
        pixels[new_top] = (0,0,0)
        if last_bottom > -1:
            pixels[last_bottom] = (0,0,0)
        if new_bottom > -1:
            pixels[new_bottom] = (0,0,0)
        
        last_top = new_top
        last_bottom = new_bottom

        new_top -= 1
        new_bottom += 1

        if new_top < MIDDLE:
            print("reset top")
            new_top = start_top
        if new_bottom > MIDDLE:
            print("reset bottom")
            new_bottom = start_bottom

        time.sleep(1)



def main():
    print("i'm main")
    subprocess.call("clear")
    warp_pixels()
    # print_pixels(get_pixels())

if __name__ == "__main__":
    main()