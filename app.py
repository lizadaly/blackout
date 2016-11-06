import random
from statistics import mean


import pyocr
import pyocr.builders
from PIL import Image, ImageDraw

BOX_PADDING = 10

def draw_horizontal_lines(draw, boxes, doc_bounding_box, line_height, line_spacing):
    """Draw black horizontal lines across the page _except_ for that word"""

    gridline_height = line_height + (line_spacing * 2.0)

    # Set up the grid
    lines = img.size[1] / gridline_height

    for i in range(0, int(lines)):
        y = i * gridline_height
        start_y = y + line_spacing
        if start_y < doc_bounding_box[1] or start_y > doc_bounding_box[3]:
            continue

        # By default, start/end at total length of line
        start_x = doc_bounding_box[0]
        end_x = doc_bounding_box[2]

        # For each box, check if the box falls in the current line
        # Note: this will clobber boxes on the same line, OK for now
        skip_line = False

        for i, b in enumerate(boxes):
            avoid_box = None
            last_box = boxes[i-1]
            this_box = boxes[i]
            for box in (this_box, last_box):
                if box.position[0][1] + BOX_PADDING > y - (gridline_height * 1.2) and box.position[1][1] - BOX_PADDING < y + (gridline_height * 1.2):
#                    box.position[1][1] > y and box.position[1][1] < y + (gridline_height * 2):
                    avoid_box = box
                    break
            if avoid_box:
                # This is the line we're on, so we need two lines: before and after
                start_x = doc_bounding_box[0]
                end_x = avoid_box.position[0][0] - BOX_PADDING
                draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height, boundary_index=2)
                start_x = avoid_box.position[1][0] + BOX_PADDING
                end_x = doc_bounding_box[2]
                draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height, boundary_index=0)
                skip_line = True
        if not skip_line:
            draw_line(draw, [start_x, start_y, end_x, start_y], line_height=line_height)

#    for box in boxes:
#        draw.rectangle(box.position, outline=(255, 0, 0))

def draw_line(draw, pos, line_height, boundary_index=None):
    # Draw a fuzzy line of randomish width repeat times
    repeat = 50
    line_height = int(line_height)
    default_padding = BOX_PADDING / 5 if boundary_index else BOX_PADDING

    for i in range(0, repeat):
        width = random.randrange(line_height - (default_padding * 2), line_height)
        if boundary_index == 0:
            padding = 0.1
        else:
            padding = default_padding
        pos[0] = random.uniform(pos[0] - padding, pos[0] + padding)

        padding = default_padding
        pos[1] = random.uniform(pos[1] - padding, pos[1] + padding)

        if boundary_index == 2:
            padding = 0.1
        else:
            padding = default_padding
        pos[2] = random.uniform(pos[2] - padding, pos[2] + padding)

        padding = default_padding
        pos[3] = random.uniform(pos[3] - padding, pos[3] + padding)

        opacity = 200 + i
        draw.line(pos, width=width, fill=(0, 0, 0, opacity))

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
    margin_lefts = []
    margin_rights = []
    margin_top = boxes[0].position[0][1]
    margin_bottom = boxes[-1].position[1][1]

    for box in boxes:
        margin_lefts.append(box.position[0][0])
        margin_rights.append(box.position[1][0])
        box_heights.append(box.position[1][1] - box.position[0][1])

    margin_left = min(margin_lefts)
    margin_right = max(margin_rights)

    line_height = mean(box_heights)
    line_spaces = [0]
    last_y_pos = boxes[0].position[1][1]

    # Line spacing is 10% of line_height
    line_spacing = line_height * .1

    img = Image.open(imagefile)
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)

    select_boxes = [boxes[10], boxes[30], boxes[200]]
    draw_horizontal_lines(draw, select_boxes,
                          doc_bounding_box=(margin_left, margin_top, margin_right, margin_bottom),
                          line_height=line_height, line_spacing=line_spacing)
    img.save("out.png")
