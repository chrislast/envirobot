import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path
from time import sleep

import ST7735

if len(sys.argv) == 1:
  MESSAGE = "Hello World! How are you today?"
else:
  MESSAGE = sys.argv[1]

# Create ST7735 LCD display class.
DISP = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    rotation=90,
    spi_speed_hz=10000000
)

# Initialize display.
DISP.begin()

WIDTH = DISP.width
HEIGHT = DISP.height

TEXT = Path("/home/pi/envirotext.txt")
MODE = Path("/home/pi/enviromode.txt")

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)


def banner(txt, mode):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    size_x, size_y = draw.textsize(txt, FONT)
    text_x = 160
    text_y = (80 - size_y) // 2

    for x in range(0,size_x + text_x + 1,2):
        if x >= size_x + text_x or int(MODE.read_text()) != mode:
            break
        draw.rectangle((0, 0, 160, 80), (0, 0, 0))
        draw.text((int(text_x - x), text_y), txt, font=FONT, fill=(255, 255, 255))
        DISP.display(img)

def show(txt, bg=(0,0,0), fg=(255,255,255)):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg)
    draw = ImageDraw.Draw(img)
    size_x, size_y = draw.textsize(txt, FONT)
    text_x = 80 - size_x // 2
    text_y = (80 - size_y) // 2
    draw.text((text_x, text_y), txt, font=FONT, fill=fg)
    DISP.display(img)


def main():

    lastmode = -1

    while not MODE.exists():
        sleep(1)

    while True:

        mode = int(MODE.read_text())

        if mode == 0 and lastmode != 0:
            DISP.clear()

        elif mode == 1 and lastmode != 1:
            show("MODE 1")

        elif mode == 2 and lastmode != 2:
            show("MODE 2", bg=(255,255,255), fg=(0,0,0))

        elif mode == 3 and lastmode != 3:
            show("MODE 3", fg=(0,255,255))

        elif mode == 4:
            if TEXT.exists():
                banner(TEXT.read_text(), mode)
            else:
                banner(MESSAGE, mode)

        else:
            sleep(0.1)

        lastmode = mode


if __name__ == "__main__":
    main()
