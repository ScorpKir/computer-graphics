import random


def menu():
    '''Функция выводит список действий для пользователя и принимает команду.'''

    menu = [
        '1. Сгенерировать случайные точки\n',
        '2. Ввести точки из файла\n',
        '-------------------------------------------------------\n',
        'Чтобы выйти из программы нажмите любую другую клавишу!\n'
    ]

    print(''.join(menu))
    return input()


def wait_key():
    input('Введите любую клавишу для продолжения: \n')


def generate_random_points(number_of_points: int) -> list[tuple[int]]:
    '''
    Функция генерирует некоторое количество случайных точек
    с диопазоном координат от -10 до 10

    :param number_of_points: количество точек для генерации

    :result: координаты точек
    '''

    points = []
    for _ in range(number_of_points):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        points.append((x, y))

    return points


def read_file_points():
    print('Тут должно быть чтение точек из файла\n')


def points_to_data(points: list[tuple[int]]) -> tuple[list[int]]:
    '''
    Функция перевожит пары точек в формат,
    который принимает matplotlib

    :param points: точки для переведения

    :result: массивы под каждую координату точек
    '''

    x, y = [], []
    for item in points:
        x.append(item[0])
        y.append(item[1])

    return x, y
