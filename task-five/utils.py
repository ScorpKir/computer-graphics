import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def points_to_data(polygon):
    xdata, ydata = [], []
    for item in polygon:
        xdata.append(item[0])
        ydata.append(item[1])
    return xdata, ydata


def draw_pixel(x, y, ax, color='black'):
    ax.add_patch(Polygon([[x, y], [x+1, y], [x+1, y+1], [x, y+1]], fc=color))


def draw_field(field, ax, bias=(0, 0), color='red'):
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            if field[x, y]:
                draw_pixel(x + bias[0], y + bias[1], ax, color=color)
