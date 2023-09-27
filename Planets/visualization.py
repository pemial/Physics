import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import time
import random

from physics import * 
        
number_of_colors = 8

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]


class Artist3D(): 
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.points = dict()
        self.ax.set_xlim(-4e8, 4e8)
        self.ax.set_ylim(-4e8, 4e8)
        self.ax.set_zlim(-4e8, 4e8)

        plt.ion()    
        plt.show()
        
    def display(self, points: [MaterialPoint]): 
        self.ax.clear()
        
        for i in range(len(points)): 
            
            if points[i].name not in self.points.keys():
                self.points[points[i].name] = [[], [], []]
            else:
                self.points[points[i].name][0].append(points[i].position.x)
                self.points[points[i].name][1].append(points[i].position.y)
                self.points[points[i].name][2].append(points[i].position.z)

            self.ax.plot(self.points[points[i].name][0], self.points[points[i].name][1], self.points[points[i].name][2])  
            self.ax.scatter(points[i].position.x, points[i].position.y, points[i].position.z, c=color[i+2], s=200) # ? Need to change the norming

        plt.pause(1e-15)
        

class SysytemSimulator:
    def __init__(self, system: ClosedSystem, artist: Artist3D, update_period: float = 0.5): 
        self.model = system
        self.artist = artist
        self.begining = time.time()
        self.update_period = update_period
       
    # * sec 
    def simulate(self, duration: float): 
        
        current_time = time.time()
        
        while(self.begining + duration > current_time):
            if (time.time() - current_time) > self.update_period:
                    current_time = time.time()
                    self.artist.display([body for body in self.model.bodies])
                    self.model.update(40_600) # * Accuracy is 1/4 day or 6 hours
     
            