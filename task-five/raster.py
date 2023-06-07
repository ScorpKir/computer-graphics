import numpy as np
from transform import (
    reverse_x,
    reverse_y,
    reverse_xy,
    move_to_origin
)

def get_line_pixels(start, end):

        dx, dy = end[0] - start[0], end[1] - start[1]

        val = []
        
        sign_x = 1 if dx > 0 else -1  if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1  if dy < 0 else 0


        if dx < 0:
            dx = -dx
        if dy < 0:
            dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = start[0], start[1]

        error, t = el / 2, 0

        flag = y
        ##self.base.grid.paint2(x, y)


        while t < el:
            error -= es
            if error < 0:
                if not pdy and y != flag:
                    val.append([x, y])
                error += el
                x += sign_x
                y += sign_y
                if pdy:
                    val.append([x, y])
            else:
                x += pdx
                y += pdy
                if pdy:
                    val.append([x, y])

            t += 1

        return val

                
def line_pixels(x1=0, y1=0, x2=0, y2=0):
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1
    error, t = el/2, 0
    pixels = [[x, y, 1]]
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        pixels.append([x, y, 1])
    return pixels


def process_line(line):
    lineMoved = False
    vector_moved = (0, 0)
    lineXReversed = False
    lineYReversed = False
    lineXYReversed = False
    if line[0][0] != 0 and line[0][1] != 0:
        lineMoved = True
        vector_moved = tuple(-line[0][0:2])
        line = move_to_origin(line, *vector_moved)
    if line[1][1] < 0:
        lineXReversed = True
        line = reverse_x(line)
    if line[1][0] < 0:
        lineYReversed = True
        line = reverse_y(line)
    if line[1][1] > line[1][0]:
        lineXYReversed = True
        line = reverse_xy(line)
    pixels = line_pixels(*line[0][:-1], *line[1][:-1])
    if lineXYReversed:
        pixels = reverse_xy(pixels)
    if lineYReversed:
        pixels = reverse_y(pixels)
    if lineXReversed:
        pixels = reverse_x(pixels)
    if lineMoved:
        pixels = move_to_origin(pixels, -vector_moved[0], -vector_moved[1])
    return pixels