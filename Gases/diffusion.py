#! /usr/bin/env python3

from tkinter import *
from tkinter.ttk import *

from dataclasses import dataclass
import math
from random import randint, uniform


max_size = 1000, 1000


particle_kwargs = {
    'outline': 'green',
    'fill': 'white',
    'width': 1,
}


@dataclass
class Particle:
    id: int = 0
    radius: int = 8
    center: tuple[int, int] = (16, 16)
    mass: float = 1
    velocity: tuple[float, float] = (0, 0)

    def __str__(self):
        return f'P:({self.center})<({self.velocity})'

    def __hash__(self):
        points = ''.join([str(p) for p in self.points])
        return int(f'{self.id}{points}')

    @property
    def points(self):
        h = self.radius
        return (
            self.center[0] - h,
            self.center[1] + h,
            self.center[0] - h,
            self.center[1] + h,
        )

    def set_position(self, x=None, y=None):
        if x:
            self.center = (x, self.center[1])
        if y:
            self.center = (self.center[0], y)

    def set_velocity(self, x=None, y=None):
        if x:
            self.velocity = (x, self.velocity[1])
        if y:
            self.velocity = (self.velocity[0], y)

    def shift(self, dx: int, dy: int):
        """ Shift a particle's position by a certain fixed amount. """
        x, y = self.center
        self.set_position(x + dx, y + dy)

    def vshift(self, dv_x: float, dv_y: float):
        """ Shift a particle's velocity vector by a certain fixed amount. """
        v_x, v_y = self.velocity
        self.velocity = (v_x + dv_x, v_y + dv_y)

    def rotate(self, theta):
        """ Reflect a particle's velocity by some angle theta. """
        v_x, v_y = self.velocity
        self.set_velocity(math.cos(theta) * v_x, math.sin(theta) * v_y)


class App(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()


class Space:

    def __init__(self, master=None, n_particles=1000):
        self.master = master
        self.particles = set()
        self.obsticals = set()
        self.create(n_particles=n_particles)

    def create(self, n_particles):
        self.canvas = Canvas(self.master)

        frame_height, frame_width = self.canvas.winfo_height(), self.canvas.winfo_width()
        center_x, center_y = frame_width / 2, frame_height / 2
        r = 50
        oval = self.canvas.create_rectangle(
            100, 100, 400, 400,
            outline = "black",
            fill = "white",
            width = 2,
        )
        self.obsticals.add(oval)

        for _ in range(n_particles):
            particle = Particle()
            particle.shift(randint(0, 100), randint(0, 100))
            particle.vshift(uniform(-5, 5), uniform(-5, 5))
            particle.id =  self.canvas.create_oval(
                *particle.points,
                **particle_kwargs,
            )
            self.particles.add(particle)

#         points = [150, 100, 200, 120, 240, 180,
#                   210, 200, 150, 150, 100, 200]

#         self.canvas.create_polygon(points, outline = "blue",
#                               fill = "orange", width = 2)

        self.canvas.pack(fill = BOTH, expand = 1)

    def translate(self, particle: Particle):
        particle.shift(*particle.velocity)
        self.canvas.moveto(particle.id, *particle.center)

    def keep_within(self, particle: Particle, min_x, min_y, max_x, max_y):
        dx, dy = particle.velocity
        if particle.center[0] <= min_x:
            particle.set_position(x=min_x)
            particle.set_velocity(-dx, dy)
        elif particle.center[0] >= max_x:
            particle.set_position(x=max_x)
            particle.set_velocity(-dx, dy)
        elif particle.center[1] <= min_y:
            particle.set_position(y=min_y)
            particle.set_velocity(dx, -dy)
        elif particle.center[1] >= max_y:
            particle.set_position(y=max_y)
            particle.set_velocity(dx, -dy)

    def keep_without(self, particle: Particle, min_x, min_y, max_x, max_y):
        dx, dy = particle.velocity

        if particle.center[0] >= min_x:
#             particle.set_position(x=min_x)
            particle.set_velocity(-dx, dy)
        elif particle.center[0] <= max_x:
#             particle.set_position(x=max_x)
            particle.set_velocity(-dx, dy)
        elif particle.center[1] >= min_y:
#             particle.set_position(y=min_y)
            particle.set_velocity(dx, -dy)
        elif particle.center[1] <= max_y:
#             particle.set_position(y=max_y)
            particle.set_velocity(dx, -dy)

    def check_collisions(self, particle: Particle):
        # Check any objects in the view
        for obstical in self.obsticals:
            coordinates = self.canvas.coords(obstical)
            if particle.id in self.canvas.find_overlapping(*coordinates):
                self.keep_without(particle, *coordinates)
        # Check the bounds of the window
        frame_height, frame_width = self.canvas.winfo_height(), self.canvas.winfo_width()
        self.keep_within(particle, 0, 0, frame_width, frame_height)

    def tick(self):
        for particle in self.particles:
            #particle.vshift(uniform(-0.1, 0.1), uniform(-0.1, 0.1))
            self.check_collisions(particle)
            self.translate(particle)


def main():
    application = App()
    application.master.title('The Room')
    application.master.maxsize(*max_size)
    application.master.geometry('500x500')

    shape = Space(application.master)

    def _render(wait=10):
        shape.tick()
        application.master.after(wait, _render)

    _render(20)  
    application.mainloop()

if __name__ == '__main__':
    main()