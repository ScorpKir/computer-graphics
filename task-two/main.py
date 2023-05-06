import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import (
    Button,
    RadioButtons,
    TextBox
)

from utils import init_axes, transform, draw


CUR_REV_TYPE = ''
DEF_PATH = np.array([
    [-3, 0, 1],
    [0, 3, 1],
    [3, 0, 1],
    [0, -3, 1],
    [-3, 0, 1],
    [-1, 1, 1],
    [0, 3, 1],
    [1, 1, 1],
    [3, 0, 1],
    [1, -1, 1],
    [0, -3, 1],
    [-1, -1, 1],
    [-3, 0, 1],
    [3, 0, 1],
    [0, 3, 1],
    [0, -3, 1]
])
PATH = np.copy(DEF_PATH)
VECTOR = [0.0, 0.0]
ANGLE = 0.0


def revTypeChanged(choice):
    global CUR_REV_TYPE
    CUR_REV_TYPE = choice


def revClicked(e):
    global CUR_REV_TYPE
    global PATH
    if CUR_REV_TYPE == 'X':
        global PATH
        PATH = transform(PATH, scale=True, x=1, y=-1)
    elif CUR_REV_TYPE == 'Y':
        global PATH
        PATH = transform(PATH, scale=True, x=-1, y=1)
    else:
        global PATH
        PATH = transform(PATH, xyreverse=True)


def xentered(text):
    global VECTOR
    VECTOR[0] = float(text)


def yentered(text):
    global VECTOR
    VECTOR[1] = float(text)


def aentered(text):
    global ANGLE
    ANGLE = float(text)


def move_clicked(text):
    global PATH
    PATH = transform(PATH, move=True, x=VECTOR[0], y=VECTOR[0])
    draw(ax, PATH)


def main():
    fig, ax = plt.subplots()
    init_axes(ax)
    plt.subplots_adjust(bottom=0.2)
    revLabels = ('X', 'Y', 'Y=X')
    global CUR_REV_TYPE
    CUR_REV_TYPE = revLabels[0]

    axRevType = plt.axes([0.01, 0.05, 0.1, 0.1])
    btnRevType = RadioButtons(axRevType, revLabels)
    btnRevType.on_clicked(revTypeChanged)

    axRev = plt.axes([0.11, 0.05, 0.1, 0.1])
    btnRev = Button(axRev, 'Reverse', color='white')
    btnRev.on_clicked(revClicked)

    axx = plt.axes([0.25, 0.117, 0.1, 0.033])
    entx = TextBox(axx, 'x: ', initial='0.0')
    entx.on_submit(xentered)

    axy = plt.axes([0.25, 0.084, 0.1, 0.033])
    enty = TextBox(axy, 'y: ', initial='0.0')
    enty.on_submit(yentered)

    axa = plt.axes([0.25, 0.05, 0.1, 0.033])
    enta = TextBox(axa, 'a: ', initial='0.0')
    enta.on_submit(aentered)

    axmove = plt.axes([0.35, 0.05, 0.1, 0.1])
    btnmove = Button(axmove, 'Move', color='white')
    btnmove.on_clicked(move_clicked)


if __name__ == '__main__':
    App()
