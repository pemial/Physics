from math import sqrt

import time
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D


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
    
    def __str__(self):
     return "x:{:<25}  y:{:<25}  z:{:<25}".format(self.x, self.y, self.z)

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other, self.z / other)

    def get_distance(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    

class Planet:
    def __init__(self, name: str, position: Vector, speed: Vector, mass: float):
        self.name = name
        self.position = position
        self.speed = speed
        self.mass = mass
        
    def __str__(self):
        return "Planet {}".format(self.name)

    def get_r(self, another_planet):
        return self.position - another_planet.position

    def get_distance(self, another_planet):
        return self.get_r(another_planet).get_distance()

    def make_calculations_2body(self, moon, dt):
        F = const.G * self.mass * moon.mass / self.get_distance(moon) ** 2

        self.position += self.speed * dt
        moon.position += moon.speed * dt

        self.speed -= F / self.mass / self.get_distance(moon) * self.get_r(moon) * dt
        moon.speed += F / moon.mass / self.get_distance(moon) * self.get_r(moon) * dt

    def visualize_2body(self, moon, current_time, dt):
        moon_coord = [[moon.position.x], [moon.position.y], [moon.position.z]]
        planet_coord = [[self.position.x], [self.position.y], [self.position.z]]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-4e8, 4e8)
        ax.set_ylim(-4e8, 4e8)
        ax.set_zlim(-4e8, 4e8)

        plt.ion()    
        plt.show()

        while(True):
            self.make_calculations_2body(moon, dt)

            if time.time() - current_time > 0.1:
                current_time = time.time()

                ax.clear()

                moon_coord[0].append(moon.position.x)
                moon_coord[1].append(moon.position.y)
                moon_coord[2].append(moon.position.z)

                planet_coord[0].append(self.position.x)
                planet_coord[1].append(self.position.y)
                planet_coord[2].append(self.position.z)

                ax.plot(np.array(moon_coord[0]), np.array(moon_coord[1]), np.array(moon_coord[2]))  
                ax.plot(np.array(planet_coord[0]), np.array(planet_coord[1]), np.array(planet_coord[2]))

                ax.scatter(self.position.x, self.position.y, self.position.z, c='g', s=100)
                ax.scatter(moon.position.x, moon.position.y, moon.position.z, c='b', s=10)

                plt.pause(1e-10)

