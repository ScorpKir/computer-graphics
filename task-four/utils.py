# Коды регионов прямоугольника
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000


def polygon_to_data(polygon):
    xdata, ydata = [], []
    for item in polygon:
        xdata.append(item[0])
        ydata.append(item[1])
    return xdata, ydata


def compute_code(x, y, rectangle):

    # Распаковываем координаты прямоугольника
    x_max, y_max, x_min, y_min = rectangle

    code = INSIDE
    if x < x_min:
        # Слева от прямоугольника
        code |= LEFT
    elif x > x_max:
        # Справа от прямоугольника
        code |= RIGHT
    if y < y_min:
        # Под прямоугольником
        code |= BOTTOM
    elif y > y_max:
        # Над прямоугольником
        code |= TOP

    return code


def poly_to_rect(polygon):
    return [
        max(map(lambda x: x[0], polygon)),
        max(map(lambda x: x[1], polygon)),
        min(map(lambda x: x[0], polygon)),
        min(map(lambda x: x[1], polygon))
    ]
