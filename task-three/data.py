from typing import Tuple
import numpy as np


def points_to_data(points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Функция конвертирует массив точек в наборы данных для отрисовки"""

    xdata = np.array([])
    ydata = np.array([])

    for point in points:
        xdata = np.append(xdata, point[0])
        ydata = np.append(ydata, point[1])

    return xdata, ydata
