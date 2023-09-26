from physics import *
from visualization import *

dt = 5                    #sec
MOON_MASS = 7.36e22       #kg
PLANET_MASS = 5.9742e24   #kg
DISTANCE = 384_400_000    #meters


def main():
    current = time.time()
    
    earth = MaterialPoint(name="Earth", 
                   position=Vector(0, 0, 0), 
                   speed=Vector(0, 0, 0),
                   mass=PLANET_MASS)
    
    print(Vector(0, 1, 0) * 2)
    
    moon = MaterialPoint(name="Moon", 
                  position=Vector(DISTANCE, 0, 0),
                  speed=Vector(0, 1, 0) * sqrt(const.G * PLANET_MASS / DISTANCE) / 2,
                  mass=MOON_MASS)
    
    planet_system = ClosedSystem(bodies=[earth, moon])
    artist_3d = Artist3D()
    
    simulator = SysytemSimulator(system=planet_system, artist=artist_3d)
    simulator.simulate(duration=float(1_000_000))


if __name__ == '__main__':
    main()
