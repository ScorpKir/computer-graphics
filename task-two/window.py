import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import (
    Button,
    RadioButtons,
    TextBox
)

from transformation import (
    xy_reverse_transform,
    move_transform,
    scaling_transform,
    rotate_transform
)
from animation import Animation


class App():
    def __init__(self):
        self.move_axes = plt.axes([0.35, 0.05, 0.1, 0.1])
        self.move_button = Button(
            self.move_axes, 'Move', color='gray', hovercolor='blue')
        self.move_button.on_clicked(self.move_clicked)

        self.scale_axes = plt.axes([0.45, 0.05, 0.1, 0.1])
        self.scale_button = Button(
            self.scale_axes, 'Scale', color='gray', hovercolor='blue')
        self.scale_button.on_clicked(self.scale_clicked)

        # Кнопка поворота относительно точки
        self.rotate_axes = plt.axes([0.55, 0.05, 0.1, 0.1])
        self.rotate_button = Button(
            self.rotate_axes, 'Rotate', color='gray', hovercolor='blue')
        self.rotate_button.on_clicked(self.rotate_clicked)

        # Кнопка возврата фигуры в исходное состояние
        self.reset_axes = plt.axes([0.65, 0.05, 0.1, 0.1])
        self.reset_button = Button(
            self.reset_axes, 'Reset', color='gray', hovercolor='red')
        self.reset_button.on_clicked(self.reset_clicked)

        # Кнопка перехода ко второй части задания (вызывает отдельное окно)
        self.anim_axes = plt.axes([0.75, 0.05, 0.2, 0.1])
        self.anim_button = Button(
            self.anim_axes, 'Plane!', color='gray', hovercolor='yellow'
        )
        self.anim_button.on_clicked(self.anim_clicked)

        # Исходное состояние фигуры
        # Задано множеством точек
        self.DEFAULT_PATH = np.array([
            [-3, 0, 1],
            [0, 3, 1],
            [3, 0, 1],
            [0, -3, 1],
            [-3, 0, 1],
            [-1, 1, 1],
            [0, 3, 1],
            [1, 1, 1],
            [3, 0, 1],
            [1, -1, 1],
            [0, -3, 1],
            [-1, -1, 1],
            [-3, 0, 1],
            [3, 0, 1],
            [0, 3, 1],
            [0, -3, 1]
        ])

        # Текущее состояние фигуры (по дефолту исходное)
        self.path = np.copy(self.DEFAULT_PATH)

        # Текущие значения X и Y
        self.current_vector = np.array([
            float(self.x_entry.text),
            float(self.y_entry.text),
        ])

        # Текущий угол
        self.current_angle = float(self.angle_entry.text)

        # Запуск метода рисования фигуры
        self.draw()

        # Отображение графика
        plt.show()

    def draw(self):
        """Функция перерисовывает фигуру"""

        # Чистим график
        self.ax.clear()

        # Заново настраиваем оси
        self.init_axes()

        # Отбрасываем единицу из точек
        points = np.array(list(map(lambda x: x[:2], self.path)))

        # Строим кривую для отображения на графике
        polygon = Polygon(points, fc='none', ec='black')

        # Добавляем кривую
        self.ax.add_patch(polygon)

        # Показываем график
        plt.show()

    def y_set(self, text):
        """
        Метод - триггер на изменение значения Y

        :param text: новое значение координаты y в текстовом варианте
        """

        # Если введенное значение можно сконвертировать в тип float
        if validate_float_input(text):
            # Записываем новое значение координаты в вектор
            self.current_vector[1] = float(text)
        else:
            # Иначе записываем в поле то значение, которое было
            self.y_entry.set_val('0.0')

    def angle_set(self, text):
        """
        Метод - триггер на изменение угла

        :param text: новое значение угла в текстовом варианте
        """

        # Если введенное значение можно сконвертировать в тип float
        if validate_float_input(text):
            # Записываем новое значение угла
            self.current_angle = float(text)
        else:
            # Иначе записываем в поле то значение, которое было
            self.angle_entry.set_val('0.0')

    def move_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки переместить

        :param event: служебный параметр
        """

        # Смещаем фигуру на текущий вектор
        self.path = move_transform(self.path, *self.current_vector)

        # Перерисовываем фигуру
        self.draw()

    def scale_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки масштабировать

        :param event: служебный параметр
        """

        # Масштабируем фигуру относительно осей
        self.path = scaling_transform(self.path, *self.current_vector)

        # Перерисовываем
        self.draw()

    def rotate_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки повернуть

        :param event: служебный параметр
        """

        # Поворачиваем фигуру на угол относительно точки
        self.path = rotate_transform(
            self.path, *self.current_vector, self.current_angle)

        # Перерисовываем фигуру
        self.draw()

    def reset_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки сбросить

        :param event: служебный параметр
        """

        # Присваиваем текущему списку точек значение по умолчанию
        self.path = np.copy(self.DEFAULT_PATH)

        # Перерисовываем фигуру
        self.draw()

    def anim_clicked(self, event):
        """
        Метод - триггер на нажатие кнопки анимация

        :param event: служебный параметр
        """

        # Вызываем новое окно с анимацией
        Animation()


def validate_float_input(number: str) -> bool:
    """
    Функция проверяет текстовое значение на возможность преобразования
    в тип float

    :param number: текстовое значение для проверки

    :result: логическое значение, обозначающее возможность конвертации
    """

    # Пытаемся преобразовать
    try:
        float(number)
    except ValueError:
        # При получении ошибки возвращаем ложь
        return False
    # Если ошибка не была отловлена, значит конвертировать можно
    return True
