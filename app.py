import random
from statistics import mean
import string

import tracery
import spacy

import pyocr
import pyocr.builders
from PIL import Image, ImageDraw, ImageFilter

BOX_PADDING = 10


def draw_vertical_lines(draw, boxes, doc_bounding_box, line_width, line_spacing):
    line_weight_factor = random.choice([1, 1, 1, 1, 0.02, 0.05, 0.07, 0.1, 0.2])
    current_x = doc_bounding_box[0] + line_width / 2
    found_letter = False
    color = (0, 0, 0)
    while current_x < doc_bounding_box[2]:
        start_x = current_x
        start_y = doc_bounding_box[1]
        end_x = start_x
        end_y = doc_bounding_box[3] - line_width / 2
        skip_line = False

        bx0 = start_x
        bx1 = start_x + line_width + (line_spacing * 2)

        select_boxes = []
        for box in boxes:
            wx0 = box.position[0][0]
            wx1 = box.position[1][0]
            if bx0 < wx0 and wx1 < bx1 or \
               wx0 < bx1 and bx1 < wx1 or \
               wx0 < bx0 and bx0 < wx1:
                select_boxes.append(box)

        if select_boxes:
            y = start_y
            for box in select_boxes:
                end_y = box.position[0][1] - BOX_PADDING
                draw_line(draw, [start_x, y, start_x, end_y], line_width=line_width, boundary_index=3, line_weight_factor=line_weight_factor)
                y = box.position[1][1] + BOX_PADDING
            draw_line(draw, [start_x, y + BOX_PADDING, start_x, doc_bounding_box[3]], line_width=line_width, boundary_index=3, line_weight_factor=line_weight_factor)
        else:
           draw_line(draw, [start_x, start_y, end_x, end_y], line_width=line_width, color=color, wobble_max=1, line_weight_factor=line_weight_factor)

        current_x = start_x + line_width + (line_spacing * 2)

#    for box in boxes:
#        draw.rectangle(box.position, outline=(255, 0, 0))

def draw_horizontal_lines(draw, boxes, doc_bounding_box, line_width, line_spacing):
    """Draw black horizontal lines across the page _except_ for that word"""

    line_weight_factor = random.choice([1, 1, 1, 1, 0.02, 0.05, 0.07, 0.1, 0.2])

    gridline_width = line_width + (line_spacing * 2.0)

    # Set up the grid
    lines = img.size[1] / gridline_width

    for i in range(0, int(lines)):
        y = i * gridline_width
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
                if box.position[0][1] + BOX_PADDING > y - (gridline_width * 1.2) and box.position[1][1] - BOX_PADDING < y + (gridline_width * 1.2):
#                    box.position[1][1] > y and box.position[1][1] < y + (gridline_width * 2):
                    avoid_box = box
                    break
            if avoid_box:
                # This is the line we're on, so we need two lines: before and after
                start_x = doc_bounding_box[0]
                end_x = avoid_box.position[0][0] - BOX_PADDING
                draw_line(draw, [start_x, start_y, end_x, start_y], line_width=line_width, boundary_index=2, line_weight_factor=line_weight_factor)
                start_x = avoid_box.position[1][0] + BOX_PADDING
                end_x = doc_bounding_box[2]
                draw_line(draw, [start_x, start_y, end_x, start_y], line_width=line_width, boundary_index=0, line_weight_factor=line_weight_factor)
                skip_line = True
        if not skip_line:
            draw_line(draw, [start_x, start_y, end_x, start_y], line_width=line_width, line_weight_factor=line_weight_factor)


def draw_line(draw, pos, line_width, boundary_index=None, color=(0, 0, 0), wobble_max=5, line_weight_factor=1):
    # Draw a fuzzy line of randomish width repeat times
    repeat = 50
    line_width = int(line_width) * line_weight_factor
    default_padding = min([BOX_PADDING / wobble_max if boundary_index else BOX_PADDING, wobble_max])

    for i in range(0, repeat):
        width = int(random.uniform(line_width - (default_padding * 2.0), line_width))

        if boundary_index == 0:
            padding = 0.1
        else:
            padding = default_padding

        pos[0] = random.uniform(pos[0] - padding, pos[0] + padding)

        if boundary_index == 1:
            padding = 0.1
        else:
            padding = default_padding
        pos[1] = random.uniform(pos[1] - padding, pos[1] + padding)

        if boundary_index == 2:
            padding = 0.1
        else:
            padding = default_padding
        pos[2] = random.uniform(pos[2] - padding, pos[2] + padding)

        if boundary_index == 3:
            padding = 0.1
        else:
            padding = default_padding
        pos[3] = random.uniform(pos[3] - padding, pos[3] + padding)

        opacity = 200 + i
        draw.line(pos, width=width, fill=(*color, opacity))

def get_boxes(imagefile):
    num_words = 5
    boxes = tool.image_to_string(
        Image.open(imagefile), lang="eng",
        builder=pyocr.builders.WordBoxBuilder()
    )
    return boxes

def image_filter(img):
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def parse_words(boxes):
    words = []
    word_box = {}
    for box in boxes:
        word = box.content.strip()
        word = word.translate(str.maketrans({a:None for a in string.punctuation}))
        words.append(word)
        word_box[word] = box
    sent = ' '.join(words)
    doc = nlp(sent)
    for token in doc:
        if token.text in word_box:
            word_box[token.text].pos = token.pos_
    return words, word_box

def find_boxes_for_grammar(boxes):
    words, word_box = parse_words(boxes)
    grammar = ['DET', 'NOUN', 'VERB']
    picks = []
    word_index = 0
    for pos in grammar:
        while True:
            word = words[word_index]
            if word_box[word].pos == pos:
                print("Picking ", word)
                picks.append(word_box[word])
                break
            else:
                word_index += 1
    return picks

if __name__ == '__main__':
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    imagefile = 'data/books/vindication/0046.png'
    boxes = get_boxes(imagefile)

    nlp = spacy.load('en')

    select_boxes = find_boxes_for_grammar(boxes)


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

    line_width = mean(box_heights)
    line_spaces = [0]
    last_y_pos = boxes[0].position[1][1]

    # Line spacing is 10% of line_width
    line_spacing = line_width * .1

    src = Image.open(imagefile)
    src = src.convert('RGBA')
    img = Image.new('RGBA', (src.size[0], src.size[1]))
    draw = ImageDraw.Draw(img)


    doc_bounding_box = (margin_left, margin_top, margin_right, margin_bottom)
    draw_vertical_lines(draw, select_boxes, doc_bounding_box=doc_bounding_box, line_width=line_width, line_spacing=line_spacing)
    draw_horizontal_lines(draw, select_boxes,
                          doc_bounding_box=doc_bounding_box,
                          line_width=line_width, line_spacing=line_spacing)



    img = image_filter(img)
    out = Image.alpha_composite(src, img)
    final = Image.new('RGBA', (src.size[0], src.size[1]))
    canvas = ImageDraw.Draw(final)
    canvas.rectangle([0, 0, final.size[0], final.size[1]], fill='white')
    final = Image.alpha_composite(final, out)
    final.save("out.png")
