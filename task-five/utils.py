import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def points_to_data(polygon):
    xdata, ydata = [], []
    for item in polygon:
        xdata.append(item[0])
        ydata.append(item[1])
    return xdata, ydata


def draw_field(field, ax, bias=(0, 0)):
    points = []
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            if field[x, y]:
                points.append([x + bias[0], y + bias[1]])
    ax.scatter(*points_to_data(points), color='black')