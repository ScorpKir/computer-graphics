'''

Точка входа приложения

'''


import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from triangulation import delaunay


if __name__ == '__main__':
    # Получаем от пользователя все что нам надо
    num_points = int(input('Введите количество точек: '))
    points = np.random.randint(-100, 100, size=(num_points, 2))
    
    # Инициализируем график
    fig = plt.figure()
    cam = Camera(fig) 
    ax = fig.add_subplot()
    
    delaunay(points, ax, cam, points)
    
    # Компилируем гифку
    animation = cam.animate(interval=300, repeat=False)
    animation.save('result.gif')
    
    plt.show()