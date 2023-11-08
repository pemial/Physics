import os
import sys
import time
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Molecule(object):
    def __init__(self, molecule, position: list, velocity: list, mass, color="black"):
        self.molecule=molecule
        self.position=np.array(position)
        self.velocity=np.array(velocity)
        self.mass=mass
        self.color=color

    def set_position(self, position: list):
        self.position=np.array(position)
        
    def set_velocity(self, velocity: list):
        self.velocity=np.array(velocity)
        
    def set_color(self,color):
        self.color=color
    
    def set_mass(self,mass):
        self.mass=mass

    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return self.velocity
        
    def get_color(self):
        return self.color
        
    def get_mass(self):
        return self.mass