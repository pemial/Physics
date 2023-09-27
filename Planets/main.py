from Solar_system import *

MOON_MASS = 7.36e22       #kg
EARTH_MASS = 5.9742e24   #kg
SUN_MASS = 1.989e30       #kg
DISTANCE_MOON = 384_400_000    #meters
DISTANCE_EARTH = 150_181_218_000 #meters
EARTH_VEL = 30_000    #m/s
MOON_VEL = 1_022      #m/s

solar_system = SolarSystem(400, projection_2d=True)

# sun = Sun(solar_system, mass=1.989e30)

# planets = (
#     Planet( #Earth
#         solar_system,
#         mass=5.9742e24,
#         position=(150_181_218_000, 0, 0),
#         velocity=Vector(0, 30_000, 0),
#     )
# )


sun = Sun(solar_system, mass=10_000)
planets = (
    Planet(
        solar_system,
        mass=100,
        position=(500, 0, 0),
        velocity=(1, 5, 5),
    ),
    Planet(
        solar_system,
        mass=10,
        position=(600, 0, 0),
        velocity=(1, 0, 0)
    )
)

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
    solar_system.draw_all()
