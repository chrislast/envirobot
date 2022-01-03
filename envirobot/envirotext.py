import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path

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

def main():

    while True:
        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        ipth = Path("/home/pi/envirotext.txt")
        if ipth.exists():
            message = ipth.read_text()
        else:
            message = MESSAGE
        size_x, size_y = draw.textsize(message, font)
        text_x = 160
        text_y = (80 - size_y) // 2

        for x in range(0,size_x + text_x + 1,2):
            if x >= size_x + text_x:
                break
            draw.rectangle((0, 0, 160, 80), (0, 0, 0))
            draw.text((int(text_x - x), text_y), message, font=font, fill=(255, 255, 255))
            DISP.display(img)

if __name__ == "__main__":
    main()
