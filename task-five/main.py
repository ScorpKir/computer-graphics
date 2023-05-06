#!/usr/bin/python3

import matplotlib.pyplot as plt
from celluloid import Camera
import numpy as np

from raster import process_line
from utils import points_to_data, draw_field


def main():
    # Задаем параметры графика
    fig = plt.figure()
    cam = Camera(fig)
    ax = fig.add_subplot()
    ax.set_xlim((-20, 20))
    ax.set_ylim((-20, 20))
    ax.minorticks_on()
    ax.grid(True, which='major')
    ax.grid(True, which='minor')

    # Читаем многоугольник
    POLY = np.loadtxt('poly.txt', dtype=int)
    SIZE = len(POLY)

    # Смещаем многоугольник в первую координатную четверть
    xmin, ymin = map(min, points_to_data(POLY))
    bias = (0 if xmin >= 0 else xmin, 0 if ymin >= 0 else ymin)
    for idx in range(SIZE):
        POLY[idx][0] -= bias[0]
        POLY[idx][1] -= bias[1]

    # Начинаем с растеризациии границ
    pixels = np.vstack([process_line([POLY[idx], POLY[(idx + 1) % SIZE]])
                        for idx in range(SIZE)])

    # Находим границы поля
    xmax, ymax = map(max, points_to_data(pixels))

    # Построим поле
    field = np.zeros((xmax + 1, ymax + 1))

    # Строим изначально заданную фигуру
    for pixel in pixels:
        field[pixel[0], pixel[1]] = 1
        draw_field(field, ax, bias=bias, color='black')
        cam.snap()

    # Откидываем из поля вредные точки
    for idx in range(SIZE):
        left_sign = POLY[idx][1] - POLY[idx - 1][1]
        right_sign = POLY[idx][1] - POLY[(idx + 1) % SIZE][1]
        if left_sign * right_sign > 0:
            field[POLY[idx][0], POLY[idx][1]] = 0

    # Выполняем алгоритм
    # Попутно выполняя анимацию отрисовки
    # ориентируясь на смещение которое делалось вначале
    for y in range(ymax + 1):
        fill = False
        for x in range(xmax):
            if field[x, y] and not field[x + 1, y]:
                fill = not fill
            if fill:
                field[x, y] = 1
                draw_field(field, ax, bias=bias, color='black')
                cam.snap()

    # Отображаем анимацию
    anim = cam.animate()
    anim.save('example.gif')
    plt.show()


if __name__ == '__main__':
    main()
