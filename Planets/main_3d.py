import time

from Planet import *
dt = 10            #sec
# MOON_MASS = 7.36e22       #kg
MOON_MASS = 100
PLANET_MASS = 5.9742e24   #kg
# DISTANCE = 384_400_000    #meters
DISTANCE = 6_390_000
MOON_SPEED = 11200       #meters per seconds


def main():
    current = time.process_time_ns()
    earth = Planet(name="Earth", 
                   position=Vector(0, 0, 0),
                   speed=Vector(0, 0, 0),
                   mass=PLANET_MASS)
    moon = Planet(name="Moon", 
                  position=Vector(DISTANCE, 0, 0),
                  speed=Vector(0, 1, 0) * MOON_SPEED,
                  mass=MOON_MASS)
    
    earth.visualize_2body(moon, current, dt)



if __name__ == '__main__':
    main()
