import numpy as np
from transform import (
    reverse_x,
    reverse_xy,
    reverse_y,
    move_to_origin
)


def get_circle_pixels(x: int, y: int, r: int) -> np.ndarray:
    """
    Функция производит растеризацию окружности

    :param x: координата x центра окружности
    :param y: координата y центра окружности
    :param r: радиус окружности

    :result: массив координат пикселей
    """
    xi = 0
    yi = r
    delta = 2 - 2 * r
    error = 0

    pixels = []

    while yi >= xi:
        pixels.append([xi, yi, 1])

        if yi == xi + 1:
            yi -= 1
            xi += 1
            continue

        if delta < 0:
            error = 2 * delta + 2 * yi - 1
            if error <= 0:
                xi += 1
                delta += 2 * xi + 1
            elif error > 0:
                xi += 1
                yi -= 1
                delta += 2 * xi - 2 * yi + 2
        elif delta > 0:
            error = 2 * delta - 2 * xi - 1
            if error <= 0:
                xi += 1
                yi -= 1
                delta += 2 * xi - 2 * yi + 2
            elif error > 0:
                yi -= 1
                delta -= 2 * yi + 1
        elif delta == 0:
            xi += 1
            yi -= 1
            delta += 2 * xi - 2 * yi + 2

    pixels = np.array(pixels)
    pixels = np.vstack([pixels, reverse_xy(pixels)])
    pixels = np.vstack([pixels, reverse_x(pixels)])
    pixels = np.vstack([pixels, reverse_y(pixels)])

    print(f'{x} {y}')
    if (x, y) != (0, 0):
        pixels = move_to_origin(pixels, x, y)

    return pixels


def get_line_pixels(x1=0, y1=0, x2=0, y2=0) -> np.ndarray:
    """
    Функция производит растеризацию отрезка

    :param x1: координата x начала отрезка
    :param y1: координата y начала отрезка
    :param x2: координата x конца отрезка
    :param y2: координата y конца отрезка

    :return: массив координат пикселей
    """

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
    pixels = np.array([x, y, 1])
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
        pixels = np.vstack([pixels, np.array([x, y, 1])])
    return pixels
