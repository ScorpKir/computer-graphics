import numpy as np


def move_to_origin(points: np.ndarray, x: int, y: int) -> np.ndarray:
    """
    Функция смещает массив точек на вектор (x, y)

    :param points: массив точек для смещения
    :param x: координата x вектора
    :param y: координата y вектора

    :return: массив смещенных точек
    """

    transform_matrix = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1]
    ])
    return np.dot(points, transform_matrix)


def reverse_x(points: np.ndarray) -> np.ndarray:
    """Функция отражает массив точек относительно оси OX"""

    transform_matrix = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])
    return np.dot(points, transform_matrix)


def reverse_y(points: np.ndarray) -> np.ndarray:
    """Функция отражает массив точек относительно оси OY"""

    transform_matrix = np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    return np.dot(points, transform_matrix)


def reverse_xy(points: np.ndarray) -> np.ndarray:
    """Функция отражает массив точек относительно прямой y=x"""

    transform_matrix = np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    return np.dot(points, transform_matrix)
