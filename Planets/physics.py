from math import sqrt
# from varname import nameof

import scipy.constants as const
        

# x: m, y: m, z: m
class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        
    def __neg__(self):
        return Vector(-self.x, 
                      -self.y, 
                      -self.z)

    def __sub__(self, other):
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    def __mul__(self, multiplier: float):
        return Vector(multiplier * self.x, 
                      multiplier * self.y,  
                      multiplier * self.z)

    def __rmul__(self, multiplier: float): # commutative
        return Vector(multiplier * self.x, 
                      multiplier * self.y, 
                      multiplier * self.z)

    def __truediv__(self, divider: float):
        return Vector(self.x / divider, 
                      self.y / divider, 
                      self.z / divider)
        
    def __str__(self):
     return "x:{:<25}  y:{:<25}  z:{:<25}".format(self.x, self.y, self.z)

    def get_length(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

 
class Point: 
    def __init__(self, 
                 name: str, 
                 position: Vector, 
                 speed: Vector = Vector(+0, +0, +0)):
        self.name = name
        self.position = position
        self.speed = speed
    
    def get_r(self, another):
        return self.position - another.position
    
    def get_distance(self, another) -> float:
        return self.get_r(another).get_length()
       
    
# mass : kg,  position: m, speed: m/sec
class MaterialPoint(Point):
    def __init__(self, 
                 name: str, 
                 position: Vector,  
                 mass: float, 
                 speed: Vector=Vector(0, 0, 0)):
        super().__init__(name=name, position=position, speed=speed)
        self.mass = mass
        
    def __str__(self):
        return "Planet {}".format(self.name)
    
    def update_speed(self, increment: float):
        self.speed += increment
        
    def update_position(self, increment: float):
        self.position += increment
        
    def get_kinetic_energy(self) -> float:
        return (self.mass * self.speed.get_length() ** 2) / 2

    def add_kinetic_energy(self, dE: float):
        v = sqrt(2 * (self.get_kinetic_energy() + dE) / self.mass)
        self.speed = self.speed / self.speed.get_length() * v

    def get_potential(self) -> Vector:
        return self.mass * self.speed

    def add_potential(self, dp):
        self.speed += dp / self.mass
    
    
class ClosedSystem: 
    def __init__(self, bodies=[MaterialPoint]):
        self.bodies = bodies
        self.count = len(self.bodies)
        self.E = self.get_full_energy()
        self.p = self.get_potential()
        
    def get_mass(self) -> float:
        mass = 0
        for body in self.bodies:
            mass += body.mass
        return mass
        
    def append(self, point: MaterialPoint): 
        self.bodies.append(bodies)
        self.count = len(self.bodies)
        
    def get_full_energy(self) -> float:
        return self.get_potential_energy() + self.get_kinetic_energy()

    def get_potential_energy(self) -> float:
        U = 0
        for i in range(0, self.count):
            for j in range(0, i):
                U += -const.G * self.bodies[i].mass * self.bodies[j].mass / self.bodies[i].get_distance(self.bodies[j])
        return U

    def get_kinetic_energy(self) -> float:
        K = 0
        for body in self.bodies:
            K += body.get_kinetic_energy()
        return K
    
    def check_energy_conservation(self):
        dE = self.E - self.get_full_energy()
        K = self.get_kinetic_energy()
        for body in self.bodies:
            body.add_kinetic_energy(dE * body.get_kinetic_energy() / K)

    def get_potential(self) -> Vector:
        p = Vector(0, 0, 0)
        for body in self.bodies:
            p += body.get_potential()
        return p

    def check_potential_conservation(self):
        dp = self.p - self.get_potential()
        mass = self.get_mass()
        for body in self.bodies:
            body.add_potential(dp * body.mass / mass)
        
    def update(self, dt: float): 
        a = []
        for i in range(self.count):
            a.append(Vector(0, 0, 0))
            for j in range(self.count):
                if i != j:
                    a[i] -= (const.G * self.bodies[j].mass * self.bodies[i].get_r(self.bodies[j])) / (
                                self.bodies[j].get_distance(self.bodies[i]) ** 3)

        for i in range(self.count):
            self.bodies[i].update_speed(a[i] * dt)
            self.bodies[i].update_position(self.bodies[i].speed * dt)
        self.check_energy_conservation()
        #
                