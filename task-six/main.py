#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from celluloid import Camera
import os

from utils import (
    menu,
    generate_random_points,
    read_file_points,
    points_to_data
)
from andrew import convex_hull


def main():
    '''Точка входа приложения'''

    while True:
        command = menu()

        fig = plt.figure()
        camera = Camera(fig)
        ax = fig.add_subplot()

        if command == '1':
            number_of_points = int(input('Введите количество точек: '))
            points = generate_random_points(number_of_points)
            convex_hull(points, ax, camera)
            ax.scatter(*points_to_data(points), color='blue')
            animation = camera.animate()
            animation.save('anim.gif')
            plt.show()
            os.system('clear')
        if command == '2':
            points = read_file_points()
            convex_hull(points, ax, camera)
            ax.scatter(*points_to_data(points), color='blue')
            animation = camera.animate(interval=150)
            animation.save('anim.gif')
            plt.show()
            os.system('clear')
        else:
            break


if __name__ == '__main__':
    main()
