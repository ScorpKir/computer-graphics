import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from utils import (
    compute_code,
    poly_to_rect,
    polygon_to_data,
    TOP,
    BOTTOM,
    LEFT,
    RIGHT
)


def cohen_sutherland_clip(polygon, line, ax):

    # Настраиваем оси
    ax.set_title('Сазерленда-Коэна')
    ax.grid(True)

    # Добавляем линию и прямоугольник на график
    ax.add_line(Line2D(*polygon_to_data(line), color='blue'))
    ax.add_patch(Polygon(polygon, fc='none', ec='black'))

    # Распаковываем прямоугольник
    x_max = max(map(lambda x: x[0], polygon))
    y_max = max(map(lambda x: x[1], polygon))
    x_min = min(map(lambda x: x[0], polygon))
    y_min = min(map(lambda x: x[1], polygon))

    # Распаковываем линию
    x1, y1 = line[0]
    x2, y2 = line[1]

    # Вычисляем регионы для точек P1 и P2
    code1 = compute_code(x1, y1, poly_to_rect(polygon))
    code2 = compute_code(x2, y2, poly_to_rect(polygon))
    accept = False

    while True:

        # Оба конца внутри прямоугольника
        if code1 == 0 and code2 == 0:
            accept = True
            break

        # Оба конца вне прямоугольника
        elif (code1 & code2) != 0:
            break

        # Какая то часть отрезка вне прямоугольника
        else:

            # Отрезок нуждается в отсечении
            # Как минимум одна точка вне прямоугольника
            # Выбираем ее
            x = 1.0
            y = 1.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # Найдем точку пересечения используя формулы
            # y = y1 + slope * (x - x1),
            # x = x1 + (1 / slope) * (y - y1)
            if code_out & TOP:

                # Над прямоугольником
                x = x1 + (x2 - x1) * \
                    (y_max - y1) / (y2 - y1)
                y = y_max

            elif code_out & BOTTOM:

                # Под прямоугольником
                x = x1 + (x2 - x1) * \
                    (y_min - y1) / (y2 - y1)
                y = y_min

            elif code_out & RIGHT:

                # Справа от прямоугольника
                y = y1 + (y2 - y1) * \
                    (x_max - x1) / (x2 - x1)
                x = x_max

            elif code_out & LEFT:

                # Слева от прямоугольника
                y = y1 + (y2 - y1) * \
                    (x_min - x1) / (x2 - x1)
                x = x_min

            # Точка пересечения найдена
            # Заменим точку вне прямоугольника на точку пересечения
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = compute_code(x1, y1, [x_max, y_max, x_min, y_min])

            else:
                x2 = x
                y2 = y
                code2 = compute_code(x2, y2, [x_max, y_max, x_min, y_min])

    if accept:
        ax.scatter([x1, x2], [y1, y2], color='green', zorder=10)
        ax.add_line(Line2D([x1, x2], [y1, y2], color='red'))
