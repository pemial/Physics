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
     return "x:{:<2}  y:{:<2}  z:{:<2}".format(self.x, self.y, self.z)

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other, self.z / other)

    def get_distance(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        return self / self.get_distance()
    

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
        # parameters
        CALC_PER_CYCLE = 100
        POINTS_TO_DRAW = 800
        PNT_NS_DELTA = 1e4
        DRAW_NS_DELTA = 1e8
        XLIM = 5e7
        YLIM = 5e7
        PATH_PNT_SIZE = 2
        EARTH_PNT_SIZE = 100
        MOON_PNT_SIZE = 10
        FIGSIZE = 7
        CRITICAL_DISTANCE = 6_371_000

        moon_coord = [[moon.position.x], [moon.position.y]]
        planet_coord = [[self.position.x], [self.position.y]]

        plt.rcParams["figure.figsize"] = (FIGSIZE, FIGSIZE)
        plt.rcParams["axes.grid"] = False

        fig = plt.figure()
        ax = fig.add_subplot(111)
        earth_circle = plt.Circle((self.position.x, self.position.y), radius=CRITICAL_DISTANCE, alpha=.3)

        current_pnt_time = time.process_time_ns()
        lab_time_day = 0

        init_full_energy = ((-1 * const.G * self.mass * moon.mass
                            / self.get_distance(moon))
                            + self.mass * (self.speed.get_distance() ** 2) / 2
                            + moon.mass * (moon.speed.get_distance() ** 2) / 2)

        #####


        init_impulse = self.mass * self.speed + moon.mass * moon.speed
        init_impulse_abs = init_impulse.get_distance()

        print(init_full_energy)

        while True:
            for i in range(CALC_PER_CYCLE):
                self.make_calculations_2body(moon, dt)

            lab_time_day += dt * CALC_PER_CYCLE / 3600 / 24

            if time.process_time_ns() - current_pnt_time >= PNT_NS_DELTA:
                current_pnt_time = time.process_time_ns()
                moon_coord[0].append(moon.position.x)
                moon_coord[1].append(moon.position.y)
                planet_coord[0].append(self.position.x)
                planet_coord[1].append(self.position.y)

            if lab_time_day > 400 and time.process_time_ns() - current_time >= DRAW_NS_DELTA:
                # print("########################################")
                # print(-1 * const.G * self.mass * moon.mass / self.get_distance(
                #     moon))
                # print(self.mass * (self.speed.get_distance() ** 2) / 2)
                # print(moon.mass * (moon.speed.get_distance() ** 2) / 2)
                # print(moon.speed.get_distance())
                # print("########################################")


                full_energy = (((-1 * const.G * self.mass * moon.mass
                                 / self.get_distance(moon))
                                + self.mass * (self.speed.get_distance() ** 2) / 2)
                               + moon.mass * (moon.speed.get_distance() ** 2) / 2)
                print(full_energy)
                energy_delta = ((full_energy - init_full_energy)
                                   / init_full_energy) * 100

                impulse = self.mass * self.speed + moon.mass * moon.speed
                impulse_abs = impulse.get_distance()
                impulse_delta = abs((impulse_abs - init_impulse_abs)
                                    / init_impulse_abs) * 100

                current_time = time.process_time_ns()

                ax.clear()
                ax.set_xlim(-XLIM, XLIM)
                ax.set_ylim(-YLIM, YLIM)
                plt.xticks(np.arange(-XLIM, XLIM + 1, 2 * XLIM / 10))
                plt.yticks(np.arange(-YLIM, YLIM + 1, 2 * YLIM / 10))
                plt.xlabel(f"Laboratory time in days: {lab_time_day:.8f}\n"
                           f"Full energy fluct: {energy_delta:.8f}%\n"
                           f"Impulse abs fluct: {impulse_delta:.14f}%\n"
                           f"Distance: {(self.get_distance(moon) - CRITICAL_DISTANCE)/ 1000:.0f} km",
                           fontsize=8)
                ax.add_artist(earth_circle)

                # may be better in terms of memory but worse in speed, need to check
                # moon_coord[0] = moon_coord[0][-POINTS_TO_DRAW:]
                # moon_coord[1] = moon_coord[1][-POINTS_TO_DRAW:]
                # planet_coord[0] = planet_coord[0][-POINTS_TO_DRAW:]
                # planet_coord[1] = planet_coord[1][-POINTS_TO_DRAW:]
                #
                # ax.scatter(np.array(moon_coord[0]),
                #            np.array(moon_coord[1]), c='gray',
                #            s=PATH_PNT_SIZE)
                # ax.scatter(np.array(planet_coord[0]),
                #            np.array(planet_coord[1]),
                #            c='gray', s=PATH_PNT_SIZE)

                # point plot
                # ax.scatter(np.array(moon_coord[0][-POINTS_TO_DRAW:]),
                #            np.array(moon_coord[1][-POINTS_TO_DRAW:]),
                #            c='gray', s=PATH_PNT_SIZE)
                # ax.scatter(np.array(planet_coord[0][-POINTS_TO_DRAW:]),
                #            np.array(planet_coord[1][-POINTS_TO_DRAW:]),
                #            c='gray', s=PATH_PNT_SIZE)

                # line plot
                ax.plot(np.array(moon_coord[0][-POINTS_TO_DRAW:]),
                           np.array(moon_coord[1][-POINTS_TO_DRAW:]),
                           c='gray')
                ax.plot(np.array(planet_coord[0][-POINTS_TO_DRAW:]),
                           np.array(planet_coord[1][-POINTS_TO_DRAW:]),
                           c='gray')

                ax.scatter(self.position.x, self.position.y, c='green',
                           s=EARTH_PNT_SIZE)
                ax.scatter(moon.position.x, moon.position.y, c='blue',
                           s=MOON_PNT_SIZE)

                plt.pause(1e-10)

                if self.get_distance(moon) < CRITICAL_DISTANCE:
                    plt.show()
                    break;

