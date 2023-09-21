from Planet import *
from math import sqrt
from varname import nameof

import time
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt

dt = 30


def main():
    cur = time.time()
    earth = Planet(name="Earth", 
                   position=Vector(0, 0, 0), 
                   speed=Vector(0, 0, 0), 
                   mass=10_000)
    moon = Planet(name="Moon", 
                  position=Vector(3, 0, 0), 
                  speed=Vector(0, sqrt(const.G  * 10_000 / 3), 0),
                  mass=1)
    
    print(sqrt(const.G * 100_000 / 10))

    fig, ax = plt.subplots()

    x = [3]
    y = [0]
    
    print("{:<85} {:<10}".format(earth.name, moon.name))

    while(True):
        F = const.G * earth.mass * moon.mass / earth.get_distance(moon) ** 2

        earth.position += earth.speed * dt
        moon.position += moon.speed * dt

        earth.speed -= F / earth.mass / earth.get_distance(moon) * earth.get_r(moon) * dt
        moon.speed += F / moon.mass / earth.get_distance(moon) * earth.get_r(moon) * dt

        if time.time() - cur > 0.5:
            print(earth.position, moon.position)
            cur = time.time()

        ax.clear()
        ln, = ax.plot(x, y, '-')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)

        x.append(moon.position.x)
        y.append(moon.position.y)

        ln.set_data(x, y)

        plt.scatter(earth.position.x, earth.position.y)
        plt.scatter(moon.position.x, moon.position.y)
        plt.pause(1e-5)
    plt.show()


if __name__ == '__main__':
    main()
