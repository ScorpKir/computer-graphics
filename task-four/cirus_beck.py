import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from utils import polygon_to_data


def dot_points(a, b): return a[0] * b[0] + a[1] * b[1]
def sub_points(a, b): return [a[0] - b[0], a[1] - b[1]]
def norm(a, b): return [a[1] - b[1], b[0] - a[0]]


def cyrus_beck_clip(polygon, line, ax):

    # Настраиваем оси
    ax.set_title('Цирус-Бек')
    ax.grid(True)

    # Добавляем линию и прямоугольник на график
    ax.add_line(Line2D(*polygon_to_data(line), color='blue'))
    ax.add_patch(Polygon(polygon, fc='none', ec='black'))

    # Если по факту в линию была передана точка то ее и возвращаем
    if line[0] == line[1]:
        return [line[0]]

    # Количество вершин полигона
    SIZE = len(polygon)

    # Вычисляем нормали для каждого сегмента
    normals = [norm(polygon[idx], polygon[(idx + 1) % SIZE])
               for idx in range(SIZE)]

    # Вычисляем разность концов отрезка
    p1_p0 = sub_points(*line[::-1])

    # Значения t
    # Значения входящих и выходящих t
    # В зависимости от знаменателя
    t, te, tl = [], [0], [1]

    # Вычисляем разности между началом отрезка и вершинами многоугольника
    p0_pei = [sub_points(polygon[idx], line[0]) for idx in range(SIZE)]

    # Значения t
    # Значения входящих и выходящих t
    # В зависимости от знаменателя
    t, te, tl = [], [0], [1]

    # Вычисляем t, te и tl
    for idx in range(SIZE):
        numerator = dot_points(normals[idx], p0_pei[idx])
        denominator = dot_points(normals[idx], p1_p0)

        t.append(numerator / denominator if denominator != 0 else 0)

        if denominator > 0:
            ax.scatter(line[0][0] + p1_p0[0] * t[idx], line[0]
                       [1] + p1_p0[1] * t[idx], color='red', zorder=10)
            te.append(t[idx])
        elif denominator < 0:
            ax.scatter(line[0][0] + p1_p0[0] * t[idx], line[0]
                       [1] + p1_p0[1] * t[idx], color='green', zorder=10)
            tl.append(t[idx])

    # Вычисляем параметры t для левой и правой точки
    temp = [max(te), min(tl)]

    # Входящее t не может быть больше выходящего t
    if temp[0] > temp[1]:
        return

    # Рисуем отсеченный отрезок
    ax.add_line(Line2D(
        [line[0][0] + p1_p0[0] * temp[0], line[0][0] + p1_p0[0] * temp[1]],
        [line[0][1] + p1_p0[1] * temp[0], line[0][1] + p1_p0[1] * temp[1]],
        color='red'
    ))
