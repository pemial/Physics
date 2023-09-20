from math import sqrt


class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    def __mul__(self, other: float):
        return Vector(other * self.x, other * self.y,  other * self.z)

    def __rmul__(self, other: float):
        return Vector(other * self.x, other * self.y, other * self.z)

    def get_distance(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


class Planet:
    def __init__(self, position: Vector, speed: Vector, mass: float):
        self.position = position
        self.speed = speed
        self.mass = mass

    def get_r(self, another_planet):
        return self.position - another_planet.position

    def get_distance(self, another_planet):
        return self.get_r(another_planet).get_distance()

