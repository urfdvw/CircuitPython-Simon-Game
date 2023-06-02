import board
import displayio
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font

small_font_file = "/OCRA_small.pcf"
small_font = bitmap_font.load_font(small_font_file)
big_font_file = "/OCRA_big.pcf"
big_font = bitmap_font.load_font(big_font_file)

display = board.DISPLAY

group = displayio.Group()
text = bitmap_label.Label(small_font, text="Hi", x=0, y=0, color=0x0F0F0F)
group.append(text)
display.show(group)

while True:
    pass