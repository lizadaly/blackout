import random

import pyocr
import pyocr.builders
from PIL import Image, ImageDraw

tool = pyocr.get_available_tools()[0]
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))

image = 'data/books/small_0000.jpg'
boxes = tool.image_to_string(
    Image.open(image), lang="eng",
    builder=pyocr.builders.WordBoxBuilder()
)

img = Image.open(image)
draw = ImageDraw.Draw(img)

# Pick a random word
box = boxes[121]
#box = random.choice(boxes)

# Draw black horizontal lines across the page _except_ for that word
line_width = 50

lines = int(int(img.size[1]) / line_width)
for line in range(0, lines):
    y = line * line_width
    # By default, start/end at total length of line
    start_x = 0
    end_x = img.size[0]
    if box.position[0][1] >= y - line_width and box.position[1][1] <= y + line_width:
        # This is the line we're on, so we need two lines: before and after
        start_x = 0
        end_x = box.position[0][0]
        draw.line([start_x, y, end_x, y], width=line_width - 5, fill=0)
        start_x = box.position[1][0]
        end_x = img.size[0]
        draw.line([start_x, y, end_x, y], width=line_width - 5, fill=0)
        continue
    draw.line([start_x, y, end_x, y], width=line_width - 5, fill=0)

#draw.rectangle(box.position)#, fill=255)
print(box.get_unicode_string())
del draw
img.save("out.png")
