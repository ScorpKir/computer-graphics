#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

from data import points_to_data
from transform import (
    move_to_origin,
    reverse_x,
    reverse_y,
    reverse_xy
)
from rasterize import (
    get_circle_pixels,
    get_line_pixels
)


def process_line(ax):
    """
    Функция выполняет пошаговую визуализацию
    алгоритма Брезенхема для линии.
    """

    # Конфигурируем график
    ax.set_title("LINE")
    ax.minorticks_on()
    ax.grid(which='minor')
    ax.grid(which='major')

    # Флаги манипуляций с отрезком
    lineMoved = False
    vector_moved = (0, 0)
    lineXReversed = False
    lineYReversed = False
    lineXYReversed = False

    # Получаем границы отрезка
    line = np.loadtxt('line.txt')

    # Рисуем изначальный отрезок
    ax.add_line(Line2D(*points_to_data(line), color='green'))

    # Если начало прямой не совпадает с началом координат
    if tuple(line[0]) != (0, 0):
        # То перемещаем прямую к началу координат
        lineMoved = True
        vector_moved = tuple(-line[0][0:2])
        line = move_to_origin(line, *vector_moved)
        # Рисуем измененный отрезок
        ax.add_line(Line2D(*points_to_data(line), color='red'))

    # Если конец прямой ниже оси OX
    if line[1][1] < 0:
        # То отражаем прямую относительно оси OX
        lineXReversed = True
        line = reverse_x(line)
        # Рисуем измененный отрезок
        ax.add_line(Line2D(*points_to_data(line), color='blue'))

    # Если конец прямой левее оси OY
    if line[1][0] < 0:
        # То отражаем прямую относительно оси OY
        lineYReversed = True
        line = reverse_y(line)
        # Рисуем измененный отрезок
        ax.add_line(Line2D(*points_to_data(line), color='yellow'))

    # Если y > x у конца отрезка
    if line[1][1] > line[1][0]:
        # То отражаем прямую относительно прямой Y=X
        lineXYReversed = True
        line = reverse_xy(line)
        # Рисуем измененный отрезок
        ax.add_line(Line2D(*points_to_data(line), color='orange'))

    # Растеризуем измененный отрезок
    pixels = get_line_pixels(*line[0][:-1], *line[1][:-1])
    ax.scatter(*points_to_data(pixels), color='green')

    # Перемещаем пикселы в соответствии с изменениями прямой
    if lineXYReversed:
        pixels = reverse_xy(pixels)
    if lineYReversed:
        pixels = reverse_y(pixels)
    if lineXReversed:
        pixels = reverse_x(pixels)
    if lineMoved:
        pixels = move_to_origin(pixels, -vector_moved[0], -vector_moved[1])

    # Получаем пикселы для изначального отрезка
    ax.scatter(*points_to_data(pixels), color='red')


def draw_circle(ax):
    # Конфигурируем оси
    ax.set_title("CIRCLE")
    ax.minorticks_on()
    ax.grid(which='minor')
    ax.grid(which='major')

    # Читаем центр и радиус окружности из файла
    circle = np.loadtxt('circle.txt')

    # Получаем список пикселей для отображения
    pixels = get_circle_pixels(*circle)

    xdata = [x[0] for x in pixels]
    ydata = [x[1] for x in pixels]

    # Добавляем точки на график
    ax.scatter(xdata, ydata, color='green')
    ax.add_patch(Circle(circle[:2], circle[-1], color='red', fill=False))


if __name__ == '__main__':
    fig, (line, circle) = plt.subplots(1, 2)
    process_line(line)
    draw_circle(circle)
    plt.show()
