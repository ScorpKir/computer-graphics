#!/usr/bin/python3
import matplotlib.pyplot as plt
import os

from utils import (
    menu,
    wait_key,
    generate_random_points,
    read_file_points,
    points_to_data
)


def main():
    '''Точка входа приложения'''

    while True:
        command = menu()

        fig = plt.figure()
        ax = fig.add_subplot()

        match command:
            case '1':
                number_of_points = int(input('Введите количество точек: '))
                points = generate_random_points(number_of_points)
                ax.scatter(*points_to_data(points), color='blue')
                plt.show()
                os.system('clear')
            case '2':
                read_file_points()
                os.system('clear')
            case _:
                'Тут'
                break


if __name__ == '__main__':
    main()
