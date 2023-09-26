from Planet import *

dt = 5                    #sec
MOON_MASS = 7.36e22       #kg
PLANET_MASS = 5.9742e24   #kg
DISTANCE = 384_400_000    #meters


def main():
    current = time.time()
    earth = Planet(name="Earth", 
                   position=Vector(0, 0, 0), 
                   speed=Vector(0, 0, 0),
                   mass=PLANET_MASS)
    moon = Planet(name="Moon", 
                  position=Vector(DISTANCE, 0, 0),
                  speed=Vector(0, 1, 0) * sqrt(const.G * PLANET_MASS / DISTANCE) / 2,
                  mass=MOON_MASS)
    
    earth.visualize_2body(moon, current, dt)



if __name__ == '__main__':
    main()
