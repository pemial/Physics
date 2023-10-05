from physics import *
from visualization import *

MOON_MASS = 7.36e22                 # kg
EARTH_MASS = 5.9742e24              # kg
SUN_MASS = 1.98892e30               # kg
MERCURY_MASS = 3.285e23             # kg
VENUS_MASS = 4.867e24               # kg
MARS_MASS = 6.4171e23               # kg

METEORITE_MASS = 4.0e2      # kg

MOON_EARTH_DISTANCE = 3.844e8       # meters
EARTH_SUN_DISTANCE = 1.49597e11     # meters
MERCURY_SUN_DISTANCE = 6.9817e10    # meters
VENUS_SUN_DISTANCE = 1.08942e11     # meters
MARS_SUN_DISTANCE = 2.38066e11      # meters

MOON_EARTH_SPEED = 1.021e3          # m/sec
EARTH_SUN_SPEED = 2.9765e4          # m/sec
MERCURY_SUN_SPEED = 3.87e4          # m/sec
VENUS_SUN_SPEED = 3.502e4           # m/sec
MARS_SUN_SPEED = 24.13e3            # m/sec

METEORITE_SUN_SPEED = 72.0e4           # m/sec


def main():
    current = time.time()

    mercury = MaterialPoint(name="Mercury",
                            position=Vector(1, 0, 0) * MERCURY_SUN_DISTANCE,
                            speed=Vector(0, 1, 0) * MERCURY_SUN_SPEED,
                            mass=MERCURY_MASS)

    venus = MaterialPoint(name="Venus",
                          position=Vector(1, 0, 0) * VENUS_SUN_DISTANCE,
                          speed=Vector(0, 1, 0) * VENUS_SUN_SPEED,
                          mass=VENUS_MASS)

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
    
    mars = MaterialPoint(name="Mars",
                        position=Vector(1, 0, 0) * MARS_SUN_DISTANCE, 
                        speed=Vector(0, 1, 0) * MARS_SUN_SPEED,
                        mass=MARS_MASS)
    
    meteorite = MaterialPoint(name="Ьeteorite 1",
                        position=Vector(1, 1, 1) * 2 * EARTH_SUN_DISTANCE,
                        speed=Vector(-1, -0.5, -1) * METEORITE_SUN_SPEED,
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

    # planet_system = ClosedSystem(bodies=[A, B, C])
    planet_system = ClosedSystem(bodies=[sun, mercury, venus, earth, moon, mars,  meteorite])
    artist_3d = Artist3D()

    simulator = SysytemSimulator(system=planet_system, artist=artist_3d, update_period=0.1)
    simulator.simulate(duration=float(32_000_000), dt=5)


if __name__ == '__main__':
    main()