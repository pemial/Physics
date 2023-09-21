from Planet import *
from math import sqrt
from varname import nameof

import time
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

dt = 30


def main():
    cur = time.time()
    earth = Planet(name="Earth", 
                   position=Vector(0, 0, 0), 
                   speed=Vector(0, 0, 0), 
                   mass=10_000)
    moon = Planet(name="Moon", 
                  position=Vector(3, 0, 2), 
                  speed=Vector(0, sqrt(const.G  * 10_000 / 3) / 1.1, 0), 
                  mass=1)
    
    print(sqrt(const.G * 100_000 / 10))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = [3]
    y = [0]
    z = [2]

    plt.ion()    ###
    plt.show()
    
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
        
        x.append(moon.position.x)
        y.append(moon.position.y)
        z.append(moon.position.z)

        ax.plot(np.array(x), np.array(y), np.array(z))    ###
        ax.scatter(earth.position.x, earth.position.y, earth.position.z, c = 'g', s=100)
        ax.scatter(moon.position.x, moon.position.y, moon.position.z, c = 'b', s=10)
         
        plt.pause(1e-5)
    plt.draw()


if __name__ == '__main__':
    main()
