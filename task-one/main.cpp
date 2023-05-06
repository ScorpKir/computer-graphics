#include <iostream>
#include <math.h>

// Класс описывает точку на плоскости
class Point2D {
  double _x, _y;

public:
  explicit Point2D(double x = 0, double y = 0) : _x(x), _y(y) {}

  inline double x() const { return _x; }
  inline double y() const { return _y; }

  friend std::istream &operator>>(std::istream &in, Point2D &p) {
    in >> p._x >> p._y;
    return in;
  }
};

// Класс описывает точку в пространстве
class Point3D {
  double _x, _y, _z;

public:
  explicit Point3D(double x = 0, double y = 0, double z = 0)
      : _x(x), _y(y), _z(z) {}

  inline double x() const { return _x; }
  inline double y() const { return _y; }
  inline double z() const { return _z; }

  friend std::istream &operator>>(std::istream &in, Point3D &p) {
    in >> p._y >> p._y >> p._z;
    return in;
  }
};

// Класс описывает прямую
class Line {
  double _a, _b, _c;

public:
  explicit Line(double a = 1, double b = 1, double c = 1)
      : _a(a), _b(b), _c(c) {}

  Line(const Point2D &p1, const Point2D &p2) {
    _a = p2.y() - p1.y();
    _b = p1.x() - p2.x();
    _c = p2.x() * p1.y() - p1.x() * p2.y();
  }

  inline double a() const { return _a; }
  inline double b() const { return _b; }
  inline double c() const { return _c; }

  friend std::istream &operator>>(std::istream &in, Line &l) {
    in >> l._a >> l._b >> l._c;
    return in;
  }
};

// Класс описывает плоскость
class Plane {
  double _a, _b, _c, _d;

public:
  explicit Plane(double a = 1, double b = 1, double c = 1, double d = 1)
      : _a(a), _b(b), _c(c), _d(d) {}

  inline double a() const { return _a; }
  inline double b() const { return _b; }
  inline double c() const { return _c; }
  inline double d() const { return _d; }

  friend std::istream &operator>>(std::istream &in, Plane &p) {
    in >> p._a >> p._b >> p._c >> p._d;
    return in;
  }
};

// Функция проверяет находится ли точка на прямой
bool checkPointOnLine(const Line l, const Point2D p, const double epsilon) {
  // Входные параметры:
  //
  // const Line l: прямая для проверки
  // const Point2D p: точка для проверки
  // const double epsilon: допустимая погрешность
  return std::fabs(l.a() * p.x() + l.b() * p.y() + l.c()) < epsilon;
}

// Функция проверяет, находится ли точка на луче, заданном другими точками
bool checkPointOnRay(const Point2D a, const Point2D b, const Point2D c,
                     const double epsilon) {
  // Входные параметры:
  //
  // const Point2D a, b: точки, по которым строится луч
  // const Point2D c: точка для проверки
  // const double epsilon: допустимая погрешность

  const Line ab = Line(a, b);

  if (!checkPointOnLine(ab, c, epsilon)) {
    return false;
  }

  if (std::fabs(ab.b()) <= epsilon) {
    if (b.y() >= a.y()) {
      return c.y() >= a.y();
    } else {
      return c.y() <= a.y();
    }
  }

  if (b.x() >= a.x()) {
    return c.x() >= a.x();
  } else {
    return c.x() <= a.x();
  }
}

// Функция проверяет, располагаются ли точки по часовой стрелке
bool checkClockwise(const Point2D a, const Point2D b, const Point2D c) {
  // Входные параметры:
  // const Point2D a, b, c: точки для проверки;
  return (b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y()) <
         0;
}

// Функция проверяет располагается ли точка на заданной плоскости
bool checkPointOnPlane(const Plane &pln, const Point3D &pnt,
                       const double epsilon) {
  // Входные параметры:
  // const Plane pln: заданная плоскость
  // const Point3D c: заданная точка
  // const double epsilon: допустимая погрешность
  return std::fabs(pln.a() * pnt.x() + pln.b() * pnt.y() + pln.c() * pnt.z() +
                   pln.d()) < epsilon;
}

// Функция выводит меню в консоль и запрашивает номер команды у пользователя
int showMenu() {
  std::cout << "1. Определить расположение точки на прямой" << std::endl
            << "2. Определить расположение точки на луче" << std::endl
            << "3. Проверить расположение по часовой стрелке у трех точек"
            << std::endl
            << "4. Проверить расположение точки на плоскости" << std::endl
            << "5. Выход" << std::endl;

  int number;
  std::cin >> number;
  return number;
}

void firstTask(const double &EPS) {
  Point2D p;
  std::cout << "Введите координаты x, y точки через пробел: ";
  std::cin >> p;

  Line l;
  std::cout << "Введите коэффициенты уравнения прямой a, b, с через пробел: ";
  std::cin >> l;

  if (checkPointOnLine(l, p, EPS)) {
    std::cout << "Точка находится на прямой" << std::endl;
  } else {
    std::cout << "Точка не находится на прямой" << std::endl;
  }
}

void secondTask(const double &EPS) {
  Point2D a;
  std::cout << "Введите координаты x, y точки A через пробел: ";
  std::cin >> a;
  Point2D b;
  std::cout << "Введите координаты x, y точки B через пробел: ";
  std::cin >> b;
  Point2D c;
  std::cout << "Введите координаты x, y точки C через пробел: ";
  std::cin >> c;

  if (checkPointOnRay(a, b, c, EPS)) {
    std::cout << "Точка C находится на луче AB" << std::endl;
  } else {
    std::cout << "Точка C не находится на луче AB" << std::endl;
  }
}

void thirdTask(const double &EPS) {
  Point2D a;
  std::cout << "Введите координаты x, y точки A через пробел: ";
  std::cin >> a;
  Point2D b;
  std::cout << "Введите координаты x, y точки B через пробел: ";
  std::cin >> b;
  Point2D c;
  std::cout << "Введите координаты x, y точки C через пробел: ";
  std::cin >> c;

  if (checkClockwise(a, b, c)) {
    std::cout << "Точки расположены по часовой стрелке" << std::endl;
  } else {
    std::cout << "Точки расположены против часовой стрелки" << std::endl;
  }
}

void fourthTask(const double &EPS) {
  Point3D pnt;
  std::cout << "Введите координаты x, y, z точки через пробел: ";
  std::cin >> pnt;

  Plane pln;
  std::cout << "Введите коэффициенты уравнения прямой a, b, с через пробел: ";
  std::cin >> pln;

  if (checkPointOnPlane(pln, pnt, EPS)) {
    std::cout << "Точка располагается на плоскости" << std::endl;
  } else {
    std::cout << "Точки не располагается на плоскости" << std::endl;
  }
}

// Функция выполняет команду, введенную пользователем
void executeCommand() {
  const int EXIT_COMMAND = 5;
  const double EPS = 1e-3;

  int command = showMenu();

  while (command != EXIT_COMMAND) {
    switch (command) {
    case 1: {
      firstTask(EPS);
      break;
    }
    case 2: {
      secondTask(EPS);
      break;
    }
    case 3: {
      thirdTask(EPS);
      break;
    }
    case 4: {
      fourthTask(EPS);
      break;
    }
    default:
      std::cout << "Введена неверная команда, попробуйте еще раз" << std::endl;
      break;
    }

    std::cout << "-------------------------------------------------------"
              << std::endl;
    command = showMenu();
  }
}

int main() { executeCommand(); }
