from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from utils import points_to_data

def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def line_by_points(point0, point1):
    a = point1[1] - point0[1]
    b = point0[0] - point1[0]
    c = point1[0] * point0[1] - point0[0] * point1[1]
    
    return a, b, c

def on_line(point, a, b, c):
    return (point[0] * a + point[1] * b + c) >= 0

def convex_hull(points, ax, cam):
    # Сортируем точки
    points = sorted(set(points))
    
    left_point = points[0]
    right_point = points[0]
    for point in points:
        if point[0] < left_point[0]:
            left_point = point
        if point[0] > right_point[0]:
            right_point = point
            
    ln = line_by_points(left_point, right_point)
    upper_points = sorted(set([item for item in points if on_line(item, *ln)]))
    lower_points = sorted(set([item for item in points if not on_line(item, *ln)]), reverse=True)
    
    # Нельзя передавать 1 или меньше точек
    if len(points) <= 1 or len(upper_points) <= 1 or len(lower_points) <= 1:
        return points
    
    # Строим нижнюю оболочку 
    lower = []
    for p in lower_points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
        
        if len(lower) > 1:
            size = len(lower)
            for idx in range(size):
                line = [lower[idx], lower[(idx + 1) % size]]
                ax.add_line(Line2D(*points_to_data(line), color='red'))
            cam.snap()
        

    # Строим верхнюю оболочку
    upper = []
    for p in upper_points:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
        
        if len(upper) > 1:
            ax.add_patch(Polygon(lower, fc='none', ec='red'))
            size = len(upper)
            for idx in range(size):
                line = [upper[idx], upper[(idx + 1) % size]]
                ax.add_line(Line2D(*points_to_data(line), color='green'))
            cam.snap()

    hull = lower + upper
    ax.scatter(*points_to_data(points), color='blue')
    ax.add_patch(Polygon(hull, fc='none', ec='black'))
    cam.snap()
    
    return lower[:-1] + upper[:-1]