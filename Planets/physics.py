from math import sqrt

import scipy.constants as const
        

# x: m, y: m, z: m
class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        
    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __mul__(self, multiplier: float):
        self.x *= multiplier
        self.y *= multiplier
        self.z *= multiplier
        return self

    def __rmul__(self, multiplier: float): # commutative
        self.x *= multiplier
        self.y *= multiplier
        self.z *= multiplier
        return self

    def __truediv__(self, divider: float):
        self.x /= divider
        self.y /= divider
        self.z /= divider
        return self
        
    def __str__(self):
     return "x:{:<25}  y:{:<25}  z:{:<25}".format(self.x, self.y, self.z)

    def get_distance(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

 
class Point: 
    def __init__(self, 
                 name: str, 
                 position: Vector, 
                 speed: Vector = Vector(0, 0, 0)):
        self.name = name
        self.position = position
        self.speed = speed
    
    def get_r(self, another):
        return self.position - another.position
    
    def get_distance(self, another):
        return self.get_r(another).get_distance()
       
    
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
    
    
class ClosedSystem: 
    def __init__(self, bodies=[MaterialPoint]):
        self.bodies = bodies
        self.count = len(self.bodies)
        
    def append(self, point: MaterialPoint): 
        self.bodies.append(bodies)
        self.count = len(self.bodies)
        
    def update(self, dt: float): 
        for i in range(self.count): 
            for j in range(i + 1, self.count): 
                a = - (const.G * self.bodies[j].mass * self.bodies[j].position) / self.bodies[j].get_distance(self.bodies[i])
                self.bodies[j].update_speed(a * (dt / 2))
                self.bodies[j].update_position(self.bodies[j].speed * dt)


