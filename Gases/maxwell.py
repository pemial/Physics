import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from matplotlib.animation import FuncAnimation
from client_view import * 

# Scaling factor for distance, m-1. The box dimension is therefore 1/rscale.
rscale = 5.e6
# Scale time by this factor, in s-1.
tscale = 1e9    # i.e. time will be measured in nanoseconds.

# Time step in scaled time units.
FPS = 50
dt = 1/FPS

# === Particle features ===
# Number of particles.
n = 2_000
theta = np.random.random(n) * 2 * np.pi
# Use the van der Waals radius of He, about 0.2 nm.
r_1 = 1.8e-10 * rscale
r_2 = 3.e-10 * rscale
# Take the mean speed to be the root-mean-square velocity of Ar at 300 K.
sbar_1 = 353 * rscale / tscale
sbar_2 = 300 * rscale / tscale
# He mass
m_1 = 6.645e-27
m_2 = 1.645e-26
# =========================

# Initialize the particles' positions randomly.
# pos = np.random.random((n, 2))

pos_1 = np.random.uniform(low=0, high=0.5, size=(n , 2)) 
pos_2 = np.random.uniform(low=0.5, high=1, size=(n , 2)) 

# Initialize the particles velocities with random orientations and random
# magnitudes  around the mean speed, sbar.
s0_1 = sbar_1 * np.random.random(n)
s0_2 = sbar_2 * np.random.random(n)
vel_1 = (s0_1 * np.array((np.cos(theta), np.sin(theta)))).T
vel_2 = (s0_2 * np.array((np.cos(theta), np.sin(theta)))).T

sim = MDSimulation(pos_1=pos_1, 
                   pos_2=pos_2, 
                   vel_1=vel_1, 
                   vel_2= vel_2, 
                   r_1=r_1, 
                   r_2=r_2,  
                   m_1=m_1, 
                   m_2=m_2)

# Set up the Figure and make some adjustments to improve its appearance.
DPI = 100
width, height = 1000, 500
fig = plt.figure(figsize=(width/DPI, height/DPI), dpi=DPI)
fig.subplots_adjust(left=0, right=0.97)
sim_ax = fig.add_subplot(121, aspect='equal', autoscale_on=False)
sim_ax.set_xticks([])
sim_ax.set_yticks([])
# Make the box walls a bit more substantial.
for spine in sim_ax.spines.values():
    spine.set_linewidth(2)

speed_ax = fig.add_subplot(122)
speed_ax.set_xlabel('Speed $v\,/m\,s^{-1}$')
speed_ax.set_ylabel('$f(v)$')

particles_1, = sim_ax.plot([], [], 'ro')
particles_2, = sim_ax.plot([], [], 'go')

speeds = get_speeds(sim.vel_1)

speed_hist = Histogram(speeds, 2 * sbar_1, 50, density=True)
speed_hist.draw(speed_ax)
speed_ax.set_xlim(speed_hist.left[0], speed_hist.right[-1])
ticks = np.linspace(0, 600, 7, dtype=int)
speed_ax.set_xticks(ticks * rscale/tscale)
speed_ax.set_xticklabels([str(tick) for tick in ticks])
speed_ax.set_yticks([])

fig.tight_layout()

# The 2D Maxwell-Boltzmann equilibrium distribution of speeds.
mean_KE = get_KE(speeds, m_1) / n
a = sim.m_1 / 2 / mean_KE
# Use a high-resolution grid of speed points so that the exact distribution looks smooth.
sgrid_hi = np.linspace(0, speed_hist.bins[-1], 200)
f = 2 * a * sgrid_hi * np.exp(-a * sgrid_hi**2)
mb_line, = speed_ax.plot(sgrid_hi, f, c='0.7')
# Maximum value of the 2D Maxwell-Boltzmann speed distribution.
fmax = np.sqrt(sim.m_1 / mean_KE / np.e)
speed_ax.set_ylim(0, fmax)

# For the distribution derived by averaging, take the abcissa speed points from the centre of the histogram bars.
sgrid = (speed_hist.bins[1:] + speed_hist.bins[:-1]) / 2
mb_est_line, = speed_ax.plot([], [], c='r')
mb_est = np.zeros(len(sgrid))

# A text label indicating the time and step number for each animation frame.
xlabel, ylabel = sgrid[-1] / 2, 0.8 * fmax
label = speed_ax.text(xlabel, ylabel, '$t$ = {:.1f}s, step = {:d}'.format(0, 0),
                      backgroundcolor='w')

def init_anim():
    """Initialize the animation"""
    particles_1.set_data([], [])
    particles_2.set_data([], [])

    return particles_1, particles_2, speed_hist.patch, mb_est_line, label

def animate(i):
    """Advance the animation by one step and update the frame."""
    global sim, verts, mb_est_line, mb_est
    sim.advance(dt)
    
    particles_1.set_data(sim.pos_1[:, X], sim.pos_1[:, Y])
    particles_1.set_color('g')
    particles_2.set_data(sim.pos_2[:, X], sim.pos_2[:, Y])
    particles_2.set_color('r')
    particles_1.set_markersize(0.5)
    particles_2.set_markersize(0.5)

    speeds = get_speeds(sim.vel_1)
    speed_hist.update(speeds)

    # Once the simulation has approached equilibrium a bit, start averaging
    # the speed distribution to indicate the approximation to the Maxwell-
    # Boltzmann distribution.
    if i >= IAV_START:
        mb_est += (speed_hist.hist - mb_est) / (i - IAV_START + 1)
        mb_est_line.set_data(sgrid, mb_est)

    label.set_text('$t$ = {:.1f} ns, step = {:d}'.format(i*dt, i))

    return particles_1, particles_2, speed_hist.patch, mb_est_line, label

# Only start averaging the speed distribution after frame number IAV_ST.
IAV_START = 20
# Number of frames; set to None to run until explicitly quit.
frames = 1000
anim = FuncAnimation(fig, animate, frames=frames, interval=10, blit=False,
                    init_func=init_anim)

plt.show()