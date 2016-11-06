import random
from statistics import mean


import pyocr
import pyocr.builders
from PIL import Image, ImageDraw

def draw_horizontal_lines(draw, boxes, line_height, line_spacing):
    """Draw black horizontal lines across the page _except_ for that word"""

    gridline_height = line_height + (line_spacing * 2.0)

    # Set up the grid
    lines = img.size[1] / gridline_height

    for i in range(0, int(lines)):
        y = i * gridline_height
        start_y = y + line_spacing

        # By default, start/end at total length of line
        start_x = 0
        end_x = img.size[0]

        # For each box, check if the box falls in the current line
        # Note: this will clobber boxes on the same line, OK for now
        skip_line = False

        for i, b in enumerate(boxes):
            avoid_box = None
            last_box = boxes[i-1]
            this_box = boxes[i]
            for box in (this_box, last_box):
                if box.position[0][1] > y - (gridline_height * 1.2) and box.position[1][1] < y + (gridline_height * 1.2):
#                    box.position[1][1] > y and box.position[1][1] < y + (gridline_height * 2):
                    avoid_box = box
                    break
            if avoid_box:
                # This is the line we're on, so we need two lines: before and after
                start_x = 0
                end_x = avoid_box.position[0][0]
                draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height)
                start_x = avoid_box.position[1][0]
                end_x = img.size[0]
                draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height)
                skip_line = True
        if not skip_line:
            draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height)

    for box in boxes:
        draw.rectangle(box.position, outline='#ff0000')

#draw.rectangle(box.position)#, fill=255)
def draw_line(draw, pos, line_height):
    draw.line(pos, width=int(line_height), fill=0)

def get_boxes(imagefile):
    num_words = 5
    boxes = tool.image_to_string(
        Image.open(imagefile), lang="eng",
        builder=pyocr.builders.WordBoxBuilder()
    )
    return boxes

if __name__ == '__main__':
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    imagefile = 'data/books/small_0000.jpg'
    boxes = get_boxes(imagefile)

    # Get the line height by taking the average of all the box heights
    box_heights = []
    for box in boxes:
        box_heights.append(box.position[1][1] - box.position[0][1])

    line_height = mean(box_heights)
    line_spaces = [0]
    last_y_pos = boxes[0].position[1][1]

    # Line spacing is 10% of line_height
    line_spacing = line_height * .1

    img = Image.open(imagefile)
    draw = ImageDraw.Draw(img)

    select_boxes = [boxes[10], boxes[20], boxes[30]]
    draw_horizontal_lines(draw, select_boxes, line_height=line_height, line_spacing=line_spacing)
    img.save("out.png")
