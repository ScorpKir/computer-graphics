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
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    # Построим поле
    field = np.zeros((xmax + 1, ymax + 1))

    # Строим изначально заданную фигуру
    for pixel in pixels:
        field[pixel[0], pixel[1]] = 1
    draw_field(field, ax, bias=bias, color='black')
    cam.snap()

    # Откидываем горизонтальные прямые
    for idx in range(SIZE):
        if POLY[idx][1] == POLY[(idx + 1) % SIZE][1]:
            x0, x1 = sorted([POLY[idx][0] + 1, POLY[(idx + 1) % SIZE][0]])
            for i in range(x0, x1):
                field[i][POLY[idx][1]] = 0
    draw_field(field, ax, bias=bias, color='black')
    cam.snap()
    
    # Откидываем верхушечки
    for idx in range(SIZE):
        left_diff = POLY[idx][1] - POLY[idx - 1][1]
        right_diff = POLY[idx][1] - POLY[(idx + 1) % SIZE][1]
        if left_diff * right_diff > 0:
            field[POLY[idx][0]][POLY[idx][1]] = 0
    draw_field(field, ax, bias=bias, color='black')
    cam.snap()
    
    # Откидываем прочие неприятности
    for i in range(xmax):
        for j in range(ymax):
            # Верхушки
            if i == 0 and j != 0:
                if field[i][j] and not field[i + 1][j] and field[i + 1][j - 1] and field[i][j - 1]:
                    field[i][j] = 0
            if i == xmax - 1 and j != 0:
                if field[i][j] and not field[i - 1][j] and field[i - 1][j - 1] and field[i][j - 1]:
                    field[i][j] = 0
            if i != xmax -1 and i != 0 and j != 0:
                if field[i][j] and not field[i + 1][j] and field[i + 1][j - 1] and field[i][j - 1]:
                    field[i][j] = 0
                if field[i][j] and not field[i - 1][j] and field[i - 1][j - 1] and field[i][j - 1]:
                    field[i][j] = 0
                if field[i][j] and not field[i -1][j] and not field[i + 1][j] and field[i - 1][j - 1] and field[i + 1][j - 1]:
                    field[i][j] = 0

            
            # Углубления
            if i == 0 and j != ymax - 1:
                if field[i][j] and not field[i + 1][j] and field[i + 1][j + 1] and field[i][j + 1]:
                    field[i][j] = 0
            if i == xmax - 1 and j != ymax - 1:
                if field[i][j] and not field[i - 1][j] and field[i - 1][j + 1] and field[i][j + 1]:
                    field[i][j] = 0
            if i != xmax -1 and i != 0 and j != ymax - 1:
                if field[i][j] and not field[i + 1][j] and field[i + 1][j + 1] and field[i][j + 1]:
                    field[i][j] = 0
                if field[i][j] and not field[i - 1][j] and field[i - 1][j + 1] and field[i][j + 1]:
                    field[i][j] = 0
                if field[i][j] and not field[i -1][j] and not field[i + 1][j] and field[i - 1][j + 1] and field[i + 1][j + 1]:
                    field[i][j] = 0
                if i > 1 and not field[i][j + 1] and field[i][j] and field[i][j - 1] and not field[i - 1][j - 1] and field[i - 2][j - 1]:
                    field[i][j] = 0

            # Горизонтали
            if i != xmax - 1:
                if field[i][j] and field[i + 1][j]:
                    field[i][j] = 0 
                                     
    draw_field(field, ax, bias=bias, color='black')
    cam.snap()
                        
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
    
    # Рисуем границу обратно            
    for pixel in pixels:
        field[pixel[0]][pixel[1]] = 1
    draw_field(field, ax, bias=bias, color='black')
    cam.snap()
    
    # Отображаем анимацию
    anim = cam.animate()
    anim.save('example.gif')
    plt.show()


if __name__ == '__main__':
    main()
