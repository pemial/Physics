from scipy.spatial.distance import pdist, squareform
import matplotlib.path as path
import matplotlib.patches as patches
import numpy as np

# axes
X, Y = 0, 1

def get_speeds(vel):
    """Return the magnitude of the (n,2) array of velocities, vel."""
    return np.hypot(vel[:, X], vel[:, Y])

def get_KE(speeds, m):
    """Return the total kinetic energy of all particles in scaled units."""
    return 0.5 * m * sum(speeds**2)

class MDSimulation:

    def __init__(self, pos_1, pos_2, vel_1, vel_2, r_1, r_2, m_2, m_1):
        """
        Initialize the simulation with identical, circular particles of radius
        r and mass m. The n x 2 state arrays pos and vel hold the n particles'
        positions in their rows as (x_i, y_i) and (vx_i, vy_i).

        """

        self.pos_1 = np.asarray(pos_1, dtype=float)
        self.pos_2 = np.asarray(pos_2, dtype=float)
        self.vel_1 = np.asarray(vel_1, dtype=float)
        self.vel_2 = np.asarray(vel_2, dtype=float)
        self.n = self.pos_1.shape[0] + self.pos_2.shape[0]
        self.m = self.pos_1.shape[0]
        self.r_1 = r_1
        self.r_2 = r_2
        self.m_1 = m_1
        self.m_2 = m_2
        self.nsteps = 0

    def advance(self, dt):
        """Advance the simulation by dt seconds."""

        self.nsteps += 1
        # Update the particles' positions according to their velocities.
        self.pos_1 += self.vel_1 * dt
        self.pos_2 += self.vel_2 * dt
        # Find indices for all unique collisions.
        dist = squareform(pdist(np.concatenate((self.pos_1, self.pos_2))))
        iarr, jarr = np.where((dist < 2 * self.r_1) | (dist < 2 * self.r_2))
        k = iarr < jarr
        iarr, jarr = iarr[k], jarr[k]

        # For each collision, update the velocities of the particles involved.
        for i, j in zip(iarr, jarr):
            
            pos_i, vel_i =  (self.pos_1[i], self.vel_1[i]) if i < self.m else (self.pos_2[i - self.m], self.vel_2[i - self.m])
            pos_j, vel_j =  (self.pos_1[j], self.vel_1[j]) if j < self.m else (self.pos_2[j - self.m], self.vel_2[j - self.m])
            
            rel_pos, rel_vel = pos_i - pos_j, vel_i - vel_j
            r_rel = rel_pos @ rel_pos
            v_rel = rel_vel @ rel_pos
            v_rel = 2 * rel_pos * v_rel / r_rel - rel_vel
            v_cm = (vel_i + vel_j) / 2
            
            if i < self.m:
                self.vel_1[i] = v_cm - v_rel/2 
            else: 
                self.vel_2[i - self.m] = v_cm - v_rel/2 
            
            if j < self.m:
                self.vel_1[j] = v_cm + v_rel/2
            else: 
                self.vel_2[j - self.m] = v_cm + v_rel/2
            

        # Bounce the particles off the walls where necessary, by reflecting
        # their velocity vectors.
        hit_left_wall_1 = self.pos_1[:, X] < self.r_1
        hit_left_wall_2 = self.pos_2[:, X] < self.r_2
        hit_right_wall_1 = self.pos_1[:, X] > 1 - self.r_1
        hit_right_wall_2 = self.pos_2[:, X] > 1 - self.r_2
        hit_bottom_wall_1 = self.pos_1[:, Y] < self.r_1
        hit_bottom_wall_2= self.pos_2[:, Y] < self.r_2
        hit_top_wall_1 = self.pos_1[:, Y] > 1 - self.r_1
        hit_top_wall_2 = self.pos_2[:, Y] > 1 - self.r_2
        self.vel_1[hit_left_wall_1 | hit_right_wall_1, X] *= -1
        self.vel_2[hit_left_wall_2 | hit_right_wall_2, X] *= -1
        
        self.vel_1[hit_bottom_wall_1 | hit_top_wall_1, Y] *= -1
        self.vel_2[hit_bottom_wall_2 | hit_top_wall_2, Y] *= -1


class Histogram:
    """A class to draw a Matplotlib histogram as a collection of Patches."""

    def __init__(self, data, xmax, nbars, density=False):
        """Initialize the histogram from the data and requested bins."""
        self.nbars = nbars
        self.density = density
        self.bins = np.linspace(0, xmax, nbars)
        self.hist, bins = np.histogram(data, self.bins, density=density)
        
        self.left = np.array(bins[:-1])
        self.right = np.array(bins[1:])
        self.bottom = np.zeros(len(self.left))
        self.top = self.bottom + self.hist
        nrects = len(self.left)
        self.nverts = nrects * 5
        self.verts = np.zeros((self.nverts, 2))
        self.verts[0::5, 0] = self.left
        self.verts[0::5, 1] = self.bottom
        self.verts[1::5, 0] = self.left
        self.verts[1::5, 1] = self.top
        self.verts[2::5, 0] = self.right
        self.verts[2::5, 1] = self.top
        self.verts[3::5, 0] = self.right
        self.verts[3::5, 1] = self.bottom

    def draw(self, ax):
        """Draw the histogram by adding appropriate patches to Axes ax."""
        codes = np.ones(self.nverts, int) * path.Path.LINETO
        codes[0::5] = path.Path.MOVETO
        codes[4::5] = path.Path.CLOSEPOLY
        barpath = path.Path(self.verts, codes)
        self.patch = patches.PathPatch(barpath, fc='tab:green', ec='k',
                                  lw=0.5, alpha=0.5)
        ax.add_patch(self.patch)

    def update(self, data):
        """Update the rectangle vertices using a new histogram from data."""
        self.hist, bins = np.histogram(data, self.bins, density=self.density)
        self.top = self.bottom + self.hist
        self.verts[1::5, 1] = self.top
        self.verts[2::5, 1] = self.top
        