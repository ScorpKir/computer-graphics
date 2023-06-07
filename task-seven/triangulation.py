"""

Алгоритм построения триангуляции Делоне для множества точек методом "Разделяй и властвуй"

"""

import numpy as np
from matplotlib.lines import Line2D


edges = []


def delaunay(S, ax, cam, points):
    '''
    Фукнция предназначена для импорта!
    
    Выполняет триангуляцию Делоне
    
    :param S: множество точек
    :param ax: ссылка на график для рисования
    :param cam: выполнятель анимации
    :param points: все точки множества
    
    :result: множество ребер, составляющих триангуляцию
    '''

    if len(S) < 2:
        print("Must be at least two points.")
        return
    
    global edges
    edges = []
    S = np.asarray(S, dtype=np.float64)
    
    # Сортируем точки сначала по координате x а затем по координате y
    S.view(dtype=[('f0', S.dtype), ('f1', S.dtype)]).sort(order=['f0', 'f1'], axis=0)
    
    # Удаляем повторяющиеся точки
    dupes = [i for i in range(1, len(S)) if S[i-1][0] == S[i][0] and S[i-1][1] == S[i][1]]
    if dupes:
        S = np.delete(S, dupes, 0)

    triangulate(S, ax, cam, points)
    ax.scatter(points[:, 0], points[:, 1], color='black')
    edges = [e for e in edges if e.data is None]  # clean the garbage
    for edge in edges:
        xdata = [edge.org[0], edge.dest[0]]
        ydata = [edge.org[1], edge.dest[1]]
        ax.add_line(Line2D(xdata, ydata, color='purple'))
    cam.snap()


# -----------------------------------------------------------------
# Структура данных ребра


class Edge:
    """
    Класс реализует направленный отрезок вида org -> dest
    
    При обходе кромочного кольца:
        Next - против часовой стрелки
        Prev - по часовой стрелке
    """

    def __init__(self, org, dest):
        self.org   = org
        self.dest  = dest
        self.onext = None
        self.oprev = None
        self.sym   = None    # Симметричный аналог этого ребра
        self.data  = None    # Может хранить что угодно


# -----------------------------------------------------------------
# Основные процедуры триангуляции


def triangulate(S, ax, cam, points):
    """
    Вычисляет триангуляцию Делоне
    
    :param S: множество точек
    :param ax: ссылка на график для рисования
    :param cam: выполнятель анимации
    :param points: Все точки множества
    """
    if len(S) == 2:
        a = make_edge(S[0], S[1])
        return a, a.sym

    elif len(S) == 3:
        # Создает ребро a соединяющее p1 с p2 и b соединяющее p2 с p3.
        p1, p2, p3 = S[0], S[1], S[2]
        a = make_edge(p1, p2)
        b = make_edge(p2, p3)
        splice(a.sym, b)

        # Закрываем треугольник
        if right_of(p3, a):
            connect(b, a)
            return a, b.sym
        elif left_of(p3, a):
            c = connect(b, a)
            return c.sym, c
        else:  # Три точки коллинеарны
            return a, b.sym

    else:
        # Рекурсивно делим S
        m = (len(S) + 1) // 2
        L, R = S[:m], S[m:]
        ldo, ldi = triangulate(L, ax ,cam, points)
        ax.scatter(points[:, 0], points[:, 1], color='black')
        global edges
        edges = [e for e in edges if e.data is None]  # clean the garbage
        for edge in edges:
            xdata = [edge.org[0], edge.dest[0]]
            ydata = [edge.org[1], edge.dest[1]]
            ax.add_line(Line2D(xdata, ydata, color='purple'))
        cam.snap()
        rdi, rdo = triangulate(R, ax, cam, points)
        ax.scatter(points[:, 0], points[:, 1], color='black')
        edges = [e for e in edges if e.data is None]  # clean the garbage
        for edge in edges:
            xdata = [edge.org[0], edge.dest[0]]
            ydata = [edge.org[1], edge.dest[1]]
            ax.add_line(Line2D(xdata, ydata, color='purple'))
        cam.snap()

        # Вычисляем верхнюю касательную для L и R
        while True:
            if right_of(rdi.org, ldi):
                ldi = ldi.sym.onext
            elif left_of(ldi.org, rdi):
                rdi = rdi.sym.oprev
            else:
                break
            
        

        # Создаем первое соединяющее ребро
        base = connect(ldi.sym, rdi)

        if ldi.org[0] == ldo.org[0] and ldi.org[1] == ldo.org[1]:
            ldo = base
        if rdi.org[0] == rdo.org[0] and rdi.org[1] == rdo.org[1]:
            rdo = base.sym

        # Соединяем
        while True:
            rcand, lcand = base.sym.onext, base.oprev
            v_rcand, v_lcand = right_of(rcand.dest, base), right_of(lcand.dest, base)
            if not (v_rcand or v_lcand):
                break
            if v_rcand:
                while right_of(rcand.onext.dest, base) and \
                      in_circle(base.dest, base.org, rcand.dest, rcand.onext.dest) == 1:
                    t = rcand.onext
                    delete_edge(rcand)
                    rcand = t
            if v_lcand:
                while right_of(lcand.oprev.dest, base) and \
                      in_circle(base.dest, base.org, lcand.dest, lcand.oprev.dest) == 1:
                    t = lcand.oprev
                    delete_edge(lcand)
                    lcand = t
            if not v_rcand or \
               (v_lcand and in_circle(rcand.dest, rcand.org, lcand.org, lcand.dest) == 1):
                base = connect(lcand, base.sym)
            else:
                base = connect(base.sym, rcand.sym)
        return ldo, rdo


# -----------------------------------------------------------------
# Predicates


def in_circle(a, b, c, d):
    """Does d lie inside of circumcircle abc?"""
    a1, a2 = a[0]-d[0], a[1]-d[1]
    b1, b2 = b[0]-d[0], b[1]-d[1]
    c1, c2 = c[0]-d[0], c[1]-d[1]
    a3, b3, c3 = a1**2 + a2**2, b1**2 + b2**2, c1**2 + c2**2
    det = a1*b2*c3 + a2*b3*c1 + a3*b1*c2 - (a3*b2*c1 + a1*b3*c2 + a2*b1*c3)
    return det < 0


def right_of(p, e):
    """Does point p lie to the right of the line of edge e?"""
    a, b = e.org, e.dest
    det = (a[0]-p[0]) * (b[1]-p[1]) - (a[1]-p[1]) * (b[0]-p[0])
    return det > 0


def left_of(p, e):
    """Does point p lie to the left of the line of edge e?"""
    a, b = e.org, e.dest
    det = (a[0]-p[0]) * (b[1]-p[1]) - (a[1]-p[1]) * (b[0]-p[0])
    return det < 0


# -----------------------------------------------------------------
# Topological operators


def make_edge(org, dest):
    """Creates a new edge. Assumes org and dest are points."""

    global edges
    e  = Edge(org, dest)
    es = Edge(dest, org)
    e.sym, es.sym = es, e  # make edges mutually symmetrical
    e.onext, e.oprev = e, e
    es.onext, es.oprev = es, es
    edges.append(e)
    return e


def splice(a, b):
    """Combines distinct edge rings / breaks the same ring in two pieces. Merging / tearing goes
    between a and a.onext through a.org to between b and b.onext."""

    if a == b:
        print("Splicing edge with itself, ignored: {}.".format(a))
        return

    a.onext.oprev, b.onext.oprev = b, a
    a.onext, b.onext = b.onext, a.onext


def connect(a, b):
    """Adds a new edge e connecting the destination of a to the origin of b, in such a way that
    a Left = e Left = b Left after the connection is complete."""
    e = make_edge(a.dest, b.org)
    splice(e, a.sym.oprev)
    splice(e.sym, b)
    return e


def delete_edge(e):
    """Disconnects the edge e from the rest of the structure (this may cause the rest of the
    structure to fall apart in two separate components)."""
    splice(e, e.oprev)
    splice(e.sym, e.sym.oprev)
    e.data, e.sym.data = True, True