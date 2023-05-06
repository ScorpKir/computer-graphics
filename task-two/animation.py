from random import choice

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation

from transformation import rotate_transform, move_transform


class Animation:
    def __init__(self):
        """Констркутор приложения с анимацией"""

        # Задаем новый график и оси
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

        # Скрываем оси
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        # Добавляем кнопку поворота
        self.fig.subplots_adjust(bottom=0.2)
        self.rotate_axes = plt.axes([0.2, 0.05, 0.6, 0.1])
        self.rotate_button = Button(
            self.rotate_axes, 'Push me!', color='red', hovercolor='green')
        self.rotate_button.on_clicked(self.rotate_clicked)

        # Задаем граничные значения по осям
        self.ax.set(xlim=(-10, 10), ylim=(-10, 10))

        # Покоординатно задаем базовый квадрат
        self.FIRST_SQUARE = np.array([
            [-2, 12, 1],
            [-2, 10, 1],
            [0, 10, 1],
            [0, 12, 1]
        ])

        # Список всевозможных цветов
        self.COLORS = ('red', 'yellow', 'blue', 'green')

        # Список типов фигур
        self.TYPES = ('square', 's', 'g', 'stick', 't')

        # Запускаем анимацию
        self.animation = FuncAnimation(
            self.fig,
            func=self.anim_update,
            init_func=self.anim_init,
            interval=1000,
            frames=11,
            blit=True
        )

        # Показываем окошко
        plt.show()

    def create_figure(self):
        """Метод инициализирует координаты расположения фигуры и ее цвет"""

        # Выбираем цвет и тип фигуры
        current_type = choice(self.TYPES)
        self.color = choice(self.COLORS)

        # В зависимости от типа фигуры
        # Добавляем к ней дополнительные квадратики
        # Путем копирования и передвижения базового квадрата из конструктора
        match current_type:
            case 'square':
                # Квадратик
                self.figures = [
                    np.copy(self.FIRST_SQUARE),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 0, 2),
                    move_transform(self.FIRST_SQUARE, 2, 2)
                ]
            case 's':
                # Кракозябра
                self.figures = [
                    np.copy(self.FIRST_SQUARE),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 2, 2),
                    move_transform(self.FIRST_SQUARE, 4, 2)
                ]
            case 'g':
                # Повернутая буква г
                self.figures = [
                    np.copy(self.FIRST_SQUARE),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 4, 0),
                    move_transform(self.FIRST_SQUARE, 4, 2)
                ]
            case 'stick':
                # Палочка
                self.figures = [
                    np.copy(self.FIRST_SQUARE),
                    move_transform(self.FIRST_SQUARE, -2, 0),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 4, 0)
                ]
            case 't':
                # Буква Т
                self.figures = [
                    np.copy(self.FIRST_SQUARE),
                    move_transform(self.FIRST_SQUARE, 2, 0),
                    move_transform(self.FIRST_SQUARE, 2, 2),
                    move_transform(self.FIRST_SQUARE, 4, 0)
                ]

    def draw(self):
        """Метод по координатам задает фигуру и рисует ее на графике"""

        self.items = []
        for figure in self.figures:
            points = np.array(list(map(lambda item: item[:2], figure)))
            polygon = Polygon(points, fc=self.color, ec='black')
            self.items.append(polygon)
            self.ax.add_patch(polygon)
        return self.items

    def anim_init(self):
        """Функция отрисовки первого кадра анимации"""

        self.create_figure()
        return self.draw()

    def anim_update(self, i):
        """
        Функция, которая вызывается при смене кадра анимации

        :param i: номер кадра
        """

        # Передвигаем фигуру вниз на два деления
        for index, figure in enumerate(self.figures):
            self.figures[index] = move_transform(
                self.figures[index], 0, -2)
        return self.draw()

    def rotate_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки повернуть

        :param event: служебный параметр
        """

        # Выясняем где центр фигуры
        x = [point[0] for figure in self.figures for point in figure]
        y = [point[1] for figure in self.figures for point in figure]
        x = sum(x) / len(x)
        y = sum(y) / len(y)

        # Поворачиваем фигуру относительно центра на 90 градусов
        for index, figure in enumerate(self.figures):
            self.figures[index] = rotate_transform(
                self.figures[index], x, y, 90)
