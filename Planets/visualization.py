import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import time

from physics import * 
        
        
class Artist3D(): 
    def __init__(self): # update_period in sec
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
        
        for point in points: 
            
            if point.name not in self.points.keys():
                self.points[point.name] = [[], [], []]
            else:
                self.points[point.name][0].append(point.position.x)
                self.points[point.name][1].append(point.position.y)
                self.points[point.name][2].append(point.position.z)

            self.ax.plot(self.points[point.name][0], self.points[point.name][1], self.points[point.name][2])  
            self.ax.scatter(point.position.x, point.position.y, point.position.z, c='g', s=100)

        plt.pause(1e-10)
        

class SysytemSimulator:
    def __init__(self, system: ClosedSystem, artist: Artist3D, update_period: float = 0.5): 
        self.model = system
        self.artist = artist
        self.begining = time.time()
        self.update_period = update_period
       
    # sec 
    def simulate(self, duration: float): 
        
        current_time = time.time()
        
        while(self.begining + duration > current_time):
            if (time.time() - current_time) > self.update_period:
                    current_time = time.time()
                    self.artist.display([body for body in self.model.bodies])
                    self.model.update(0.1)
     
            