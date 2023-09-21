from Planet import *
from math import sqrt
from varname import nameof

import time
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

dt = 5


def main():
    cur = time.time()
    earth = Planet(name="Earth", 
                   position=Vector(0, 0, 0), 
                   speed=Vector(0, 0, 0),
                   mass=5.9742e24)
    moon = Planet(name="Moon", 
                  position=Vector(384_400_000, 0, 0),
                  speed=Vector(0, 1, 0) * sqrt(const.G * 5.9742e24 / 384_400_000) / 2,
                  mass=7.36e22)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    moonx = [moon.position.x]
    moony = [moon.position.y]
    moonz = [moon.position.z]

    earthx = [earth.position.x]
    earthy = [earth.position.y]
    earthz = [earth.position.z]

    plt.ion()    ###
    plt.show()
    
    print("{:<85} {:<10}".format(earth.name, moon.name))

    while(True):
        F = const.G * earth.mass * moon.mass / earth.get_distance(moon) ** 2

        earth.position += earth.speed * dt
        moon.position += moon.speed * dt

        earth.speed -= F / earth.mass / earth.get_distance(moon) * earth.get_r(moon) * dt
        moon.speed += F / moon.mass / earth.get_distance(moon) * earth.get_r(moon) * dt

        if time.time() - cur > 0.1:
            print(earth.position, moon.position)
            cur = time.time()

            ax.clear()

            ax.set_xlim(-4e8, 4e8)
            ax.set_ylim(-4e8, 4e8)
            ax.set_zlim(-4e8, 4e8)

            moonx.append(moon.position.x)
            moony.append(moon.position.y)
            moonz.append(moon.position.z)

            earthx.append(earth.position.x)
            earthy.append(earth.position.y)
            earthz.append(earth.position.z)

            ax.plot(np.array(moonx), np.array(moony), np.array(moonz))  ###
            ax.plot(np.array(earthx), np.array(earthy), np.array(earthz))
            ax.scatter(earth.position.x, earth.position.y, earth.position.z, c='g', s=100)
            ax.scatter(moon.position.x, moon.position.y, moon.position.z, c='b', s=10)

            plt.pause(1e-10)


    plt.draw()


if __name__ == '__main__':
    main()
