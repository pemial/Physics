from physics import *
from visualization import *

MOON_MASS = 7.36e22             # * kg
EARTH_MASS = 5.9742e24          # * kg
SUN_MASS = 1.989e30             # * kg
DISTANCE = 384_400_000          # * meters
SUN_TO_EARTH = 149_960_000_000  # * meters

def main():
    current = time.time()
    
    earth = MaterialPoint(name="Earth", 
                   position=Vector(SUN_TO_EARTH, +0, +0), 
                   speed=Vector(+0, 1, +0) * sqrt(const.G * SUN_MASS / SUN_TO_EARTH) / 2,
                   mass=EARTH_MASS)
    
    moon = MaterialPoint(name="Moon", 
                  position=Vector(SUN_TO_EARTH + DISTANCE, +0, +0),
                  speed=Vector(0, 1, 0) * sqrt(const.G * EARTH_MASS / DISTANCE) / 2,
                  mass=MOON_MASS)
    
    sun = MaterialPoint(name="Sun", 
                  position=Vector(+0, +0, +0),
                  speed=Vector(+5, +1, +3) * sqrt(const.G * MOON_MASS / DISTANCE) / 2,
                  mass=SUN_MASS)
    
    planet_system = ClosedSystem(bodies=[earth, moon, sun])
    artist_3d = Artist3D()
    
    simulator = SysytemSimulator(system=planet_system, artist=artist_3d)
    simulator.simulate(duration=float(32_000_000)) # * sec or 1 year


if __name__ == '__main__':
    main()
