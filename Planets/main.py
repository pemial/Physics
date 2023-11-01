from Solar_system import *

MOON_MASS = 7.36e22       #kg
EARTH_MASS = 5.9742e24   #kg
SUN_MASS = 1.989e30       #kg
DISTANCE_MOON = 384_400_000    #meters
DISTANCE_EARTH = 150_181_218_000 #meters
EARTH_VEL = 30_000    #m/s
MOON_VEL = 1_022      #m/s

solar_system = SolarSystem(500, projection_2d=True)

sun = Sun(solar_system)

planets = (
    Planet(
        solar_system,
        mass=10,
        position=(200, 50, 0),
        velocity=(0, 5, 5),
    ),
    Planet(
        solar_system,
        mass=5,
        position=(200, -50, 150),
        velocity=(5, 0, 0)
    )
)

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
    solar_system.draw_all()
