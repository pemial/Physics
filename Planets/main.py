from Planet import *
from math import sqrt
import time
import numpy as np
import matplotlib.pyplot as plt

G = 6.6743e-11
dt = 30


def main():
    cur = time.time()
    A = Planet(Vector(0, 0, 0), Vector(0, 0, 0), 10_000)
    B = Planet(Vector(3, 0, 0), Vector(0, sqrt(G * 10_000 / 3) / 1.1, 0), 1)
    print(sqrt(G * 100_000 / 10))

    fig, ax = plt.subplots()

    x = [3]
    y = [0]

    while(True):
        F = G * A.mass * B.mass / A.get_distance(B) ** 2

        A.position += A.speed * dt
        B.position += B.speed * dt

        A.speed -= F / A.mass / A.get_distance(B) * A.get_r(B) * dt
        B.speed += F / B.mass / A.get_distance(B) * A.get_r(B) * dt

        if time.time() - cur > 0.5:
            print(A.position.x, A.position.y, A.position.z, "      ", B.position.x, B.position.y, B.position.z)
            cur = time.time()

        ax.clear()
        ln, = ax.plot(x, y, '-')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)

        x.append(B.position.x)
        y.append(B.position.y)

        ln.set_data(x, y)

        plt.scatter(A.position.x, A.position.y)
        plt.scatter(B.position.x, B.position.y)
        plt.pause(1e-5)
    plt.show()


if __name__ == '__main__':
    main()
