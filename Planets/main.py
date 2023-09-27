from physics import *
from visualization import *

MOON_MASS = 7.36e22                 # kg
EARTH_MASS = 5.9742e24              # kg
SUN_MASS = 1.98892e30               # kg

MOON_EARTH_DISTANCE = 3.844e8       # meters
EARTH_SUN_DISTANCE = 1.49597e11     # meters

MOON_EARTH_SPEED = 1.021e3          # m/sec
EARTH_SUN_SPEED = 2.9765e4          # m/sec


def main():
    current = time.time()

    earth = MaterialPoint(name="Earth",
                          position=Vector(1, 0, 0) * EARTH_SUN_DISTANCE,
                          speed=Vector(0, 1, 0) * EARTH_SUN_SPEED,
                          mass=EARTH_MASS)

    moon = MaterialPoint(name="Moon",
                         position=Vector(1, 0, 0) * (EARTH_SUN_DISTANCE + MOON_EARTH_DISTANCE),
                         speed=Vector(0, 1, 0) * (EARTH_SUN_SPEED + MOON_EARTH_SPEED),
                         mass=MOON_MASS)

    sun = MaterialPoint(name="Sun",
                        position=Vector(0, 0, 0),
                        speed=Vector(0, 0, 0),
                        mass=SUN_MASS)

    speed = sqrt(const.G * 1 / 2)
    A = MaterialPoint(name="A",
                      position=Vector(1, 0, 0),
                      speed=Vector(1 / 2, sqrt(3) / 2, 0) * speed,
                      mass=1)

    B = MaterialPoint(name="B",
                      position=Vector(-1, 0, 0),
                      speed=Vector(1 / 2, -sqrt(3) / 2, 0) * speed,
                      mass=1)

    C = MaterialPoint(name="C",
                      position=Vector(0, sqrt(3), 0),
                      speed=Vector(-1, 0, 0) * speed,
                      mass=1)

    planet_system = ClosedSystem(bodies=[A, B, C])
    artist_3d = Artist3D()

    simulator = SysytemSimulator(system=planet_system, artist=artist_3d)
    simulator.simulate(duration=float(32_000_000))  # * sec or 1 year


if __name__ == '__main__':
    main()