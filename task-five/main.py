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
    draw_field(field, ax, bias=bias)
    cam.snap()

    # Откидываем горизонтальные прямые
    for idx in range(SIZE):
        if POLY[idx][1] == POLY[(idx + 1) % SIZE][1]:
            x0, x1 = sorted([POLY[idx][0] + 1, POLY[(idx + 1) % SIZE][0]])
            for i in range(x0, x1):
                field[i][POLY[idx][1]] = 0
    draw_field(field, ax, bias=bias)
    cam.snap()
    
    # Откидываем уголки
    pixels_count = len(pixels)
    for i in range(pixels_count):    
        i_1, i_2, i_3 = (i + 1) % pixels_count, (i + 2) % pixels_count, (i + 3) % pixels_count
        dy_base = pixels[i_1][1] - pixels[i][1]
        dy_1 = pixels[i_2][1] - pixels[i_1][1]
        dy_2 = pixels[i_3][1] - pixels[i_2][1]
        if dy_2 * dy_1 < 0:
            field[pixels[i_2][0], pixels[i_2][1]] = 0
        elif dy_2 * dy_1 == 0 and dy_2 * dy_base <= 0:
            field[pixels[i_2][0], pixels[i_2][1]] = 0
        else:
            field[pixels[i_2][0], pixels[i_2][1]] = 1
    cam.snap()
                     
    # Выполняем алгоритм
    # Попутно выполняя анимацию отрисовки
    # ориентируясь на смещение которое делалось вначале
    for y in range(ymax + 1):
        fill = False
        for x in range(xmax):
            if field[x, y]:
                fill = not fill
            if fill:
                field[x, y] = 1
                draw_field(field, ax, bias=bias)
                cam.snap()
    
    
    # Добавляем несколько кадров результата
    for item in pixels:
        field[item[0], item[1]] = 1
        
    draw_field(field, ax, bias=bias)
    cam.snap()
    draw_field(field, ax, bias=bias)
    cam.snap()
    draw_field(field, ax, bias=bias)
    cam.snap()
    
    # Отображаем анимацию
    anim = cam.animate(interval=300)
    anim.save('example.gif')
    plt.show()


if __name__ == '__main__':
    main()