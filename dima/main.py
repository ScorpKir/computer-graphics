#!/usr/bin/python

from matplotlib import pyplot
import numpy
from celluloid import Camera


def move_to_origin(points, x, y):
    matrix = numpy.array([
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1]
    ])
    return numpy.dot(points, matrix)


def reverse_x(points):
    matrix = numpy.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])
    return numpy.dot(points, matrix)


def reverse_y(points):
    matrix = numpy.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    return numpy.dot(points, matrix)


def reverse_xy(points):
    matrix = numpy.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    return numpy.dot(points, matrix)


def get_line_pixels(x1=0, y1=0, x2=0, y2=0):
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
    pixels = numpy.array([x, y, 1])
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
        pixels = numpy.vstack([pixels, numpy.array([x, y, 1])])
    return pixels


def process_line(line):
    move_flag = False
    move_coords = (0, 0)
    xreverse_flag = False
    yreverse_flag = False
    xyreverse_flag = False

    if tuple(line[0][0:2]) != (0, 0):
        move_flag = True
        move_coords = tuple(map(lambda x: -x, line[0][0:2]))
        line = move_to_origin(line, *move_coords)
    if line[1][1] < 0:
        xreverse_flag = True
        line = reverse_x(line)
    if line[1][0] < 0:
        yreverse_flag = True
        line = reverse_y(line)
    if line[1][1] > line[1][0]:
        xyreverse_flag = True
        line = reverse_xy(line)
    pixels = get_line_pixels(*line[0][:-1], *line[1][:-1])
    if xyreverse_flag:
        pixels = reverse_xy(pixels)
    if yreverse_flag:
        pixels = reverse_y(pixels)
    if xreverse_flag:
        pixels = reverse_x(pixels)
    if move_flag:
        pixels = move_to_origin(pixels, -move_coords[0], -move_coords[1])
    pixels = list(map(lambda item: item[0:2], pixels.tolist()))
    return pixels


def point_for_scatter(points):
    first, second = [], []
    for p in points:
        first.append(p[0])
        second.append(p[1])
    return first, second


comanda = 'y'
path = input('Введите название файла: ')
verchiny = numpy.loadtxt(path)
verchiny = [[*item, 1] for item in verchiny]
verchiny = numpy.array(verchiny)

print('Ваши вершины: \n' + str(verchiny) + '\n' + '-' * 40 + '\n')

zx, zy = map(int, input('Введите затравочный пиксел: ').split())
field = {'black': [], 'red': []}
stack = [[zx, zy]]
fig = pyplot.figure()
ax = fig.add_subplot()
ax.grid(True)
camera = Camera(fig)


def draw():
    global field
    ax.scatter(*point_for_scatter(field['black']), color='black')
    ax.scatter(*point_for_scatter(field['red']), color='red')


for idx in range(len(verchiny)):
    line = [verchiny[idx], verchiny[(idx + 1) % len(verchiny)]]
    field['black'].extend(process_line(line))
    draw()
    camera.snap()

while len(stack) != 0:
    point = stack.pop()
    field['red'].append(point)
    draw()
    camera.snap()
    x, y = point

    while point in stack:
        stack.remove(point)

    upper, lower = [x, y + 1], [x, y - 1]
    left, right = [x - 1, y], [x + 1, y]

    if all([
        right not in field['black'],
        right not in field['red'],
    ]):
        stack.append(right)
    if all([
        upper not in field['black'],
        upper not in field['red'],
    ]):
        stack.append(upper)
    if all([
        left not in field['black'],
        left not in field['red'],
    ]):
        stack.append(left)
    if all([
        lower not in field['black'],
        lower not in field['red'],
    ]):
        stack.append(lower)

animation = camera.animate()
animation.save('lol.gif')
pyplot.show()
