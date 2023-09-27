from math import sqrt
from varname import nameof

import scipy.constants as const


# x: m, y: m, z: m
class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector(-self.x,
                      -self.y,
                      -self.z)

    def __sub__(self, other):
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    def __mul__(self, multiplier: float):
        return Vector(multiplier * self.x,
                      multiplier * self.y,
                      multiplier * self.z)

    def __rmul__(self, multiplier: float):  # commutative
        return Vector(multiplier * self.x,
                      multiplier * self.y,
                      multiplier * self.z)

    def __truediv__(self, divider: float):
        return Vector(self.x / divider,
                      self.y / divider,
                      self.z / divider)

    def __str__(self):
        return "x:{:<25}  y:{:<25}  z:{:<25}".format(self.x, self.y, self.z)

    def get_length(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


class Point:
    def __init__(self,
                 name: str,
                 position: Vector,
                 speed: Vector = Vector(+0, +0, +0)):
        self.name = name
        self.position = position
        self.speed = speed

    def get_r(self, another):
        return self.position - another.position

    def get_distance(self, another) -> float:
        return self.get_r(another).get_length()


# mass : kg,  position: m, speed: m/sec
class MaterialPoint(Point):
    def __init__(self,
                 name: str,
                 position: Vector,
                 mass: float,
                 speed: Vector = Vector(0, 0, 0)):
        super().__init__(name=name, position=position, speed=speed)
        self.mass = mass

    def __str__(self):
        return "Planet {}".format(self.name)

    def update_speed(self, increment: float):
        self.speed += increment

    def update_position(self, increment: float):
        self.position += increment


class ClosedSystem:
    def __init__(self, bodies: [MaterialPoint]):
        self.bodies = bodies
        self.count = len(self.bodies)

    def append(self, point: MaterialPoint):
        self.bodies.append(point)
        self.count = len(self.bodies)

    def update(self, dt: float):
        a = []
        for i in range(self.count):
            a.append(Vector(0, 0, 0))
            for j in range(self.count):
                if i != j:
                    a[i] -= (const.G * self.bodies[j].mass * self.bodies[i].get_r(self.bodies[j])) / (
                                self.bodies[j].get_distance(self.bodies[i]) ** 3)

        for i in range(self.count):
            self.bodies[i].update_position(self.bodies[i].speed * dt)
        for i in range(self.count):
            self.bodies[i].update_speed(a[i] * dt)
