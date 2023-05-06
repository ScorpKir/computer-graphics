import numpy as np
from math import cos, sin, radians
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def init_axes(ax):
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set(xlim=(-10, 10), ylim=(-10, 10))
    ax.grid(True)


def transform(*args, **kwargs):
    if kwargs.get('scale'):
        x, y = kwargs.get('x'), kwargs.get('y')
        matrix = np.array([
            [x, 0, 0],
            [0, y, 0],
            [0, 0, 1]
        ])
        return np.dot(args[0], matrix)
    if kwargs.get('move'):
        x, y = kwargs.get('x'), kwargs.get('y')
        matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [x, y, 1]
        ])
        return np.dot(args[0], matrix)
    if kwargs.get('xyreverse'):
        matrix = np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        return np.dot(args[0], matrix)
    if kwargs.get('rotate'):
        x, y = kwargs.get('x'), kwargs.get('y')
        angle = radians(kwargs.get('angle'))
        matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-x, -y, 1]
        ])
        points = np.dot(args[0], matrix)
        matrix = np.array([
            [cos(angle), sin(angle), 0],
            [-sin(angle), cos(angle), 0],
            [0, 0, 1]
        ])
        points = np.dot(points, matrix)
        matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [x, y, 1]
        ])
        return np.dot(points, matrix)


def draw(ax, pnts):
    ax.clear()
    init_axes(ax)
    pnts = np.array(list(map(lambda x: x[:2], pnts)))
    poly = Polygon(pnts, fc='none', ec='black')
    ax.add_patch(poly)
    plt.show()
