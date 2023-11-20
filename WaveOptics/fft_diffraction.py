import numpy as np
from scipy.fftpack import fft2
from scipy.fftpack import fftshift
import matplotlib.pyplot as plt
import cv2


class Sheet():
    def __init__(self,extent_x, extent_y, Nx, Ny):

        self.dx = extent_x/Nx
        self.dy = extent_y/Ny

        self.x = self.dx*(np.arange(Nx) - Nx//2)
        self.y = self.dy*(np.arange(Ny) - Ny//2)
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        
        self.Nx = int(Nx)
        self.Ny = int(Ny)
        self.E = np.zeros((self.Ny, self.Nx))

        

    def rectangular_slit(self, x0, y0, lx, ly):
        """
        Creates a slit centered at the point (x0, y0) with width lx and height ly
        """
        self.E += np.select( [((self.xx > (x0 - lx/2) ) &\
                               (self.xx < (x0 + lx/2) )) &\
                              ((self.yy > (y0 - ly/2) ) &\
                               (self.yy < (y0 + ly/2) )),  True], [1, 0])
    

    def circular_aperture(self, x0, y0, r):
        """
        Creates a circular slit centered at the point (x0, y0) with radius = r
        """
        self.E += np.select( [((self.xx - x0)**2 + (self.yy - y0)**2 < r**2),  True], [1, 0])


#simulation input:

Lx = 1.5
Ly = 0.5
Nx= 1500
Ny= 1500

sheet = Sheet(extent_x = 2*Lx , extent_y = 2*Ly, Nx= Nx, Ny= Ny)
mm = 1e-3

'''circular aperture'''
sheet.circular_aperture(x0 = 0, y0 = 0, r = 10 * mm)


'''one rectangular slit'''
# sheet.rectangular_slit(x0 = 0, y0 = 0, lx = 22 * mm , ly = 88 * mm)


'''two rectangular slits'''
# D = 128 * mm

# sheet.rectangular_slit(x0 = -D/2, y0 = 0, lx = 22 * mm , ly = 88 * mm)
# sheet.rectangular_slit(x0 = +D/2, y0 = 0, lx = 22 * mm , ly = 88 * mm)


'''cross slit'''
# sheet.rectangular_slit(x0 = 0, y0 = 0, lx = 22 * mm , ly = 88 * mm)
# sheet.rectangular_slit(x0 = 0, y0 = 0, lx = 88 * mm , ly = 22 * mm)


'''SIMULATION'''
# distance from slit to the screen (mm)
z = 5000

# wavelength (mm)
λ = 18.5*1e-7
k = 2*np.pi/λ

fft_c = fft2(sheet.E * np.exp(1j * k/(2*z) *(sheet.xx**2 + sheet.yy**2)))
c = fftshift(fft_c)

fig = plt.figure(figsize=(6, 6))
ax1 = fig.add_subplot(2,1,1)  
ax2 = fig.add_subplot(2,1,2, sharex=ax1, yticklabels=[])  

abs_c = np.absolute(c)

#screen size mm
dx_screen = z*λ/(2*Lx)
dy_screen = z*λ/(2*Ly)
x_screen = dx_screen * (np.arange(Nx)-Nx//2)
y_screen = dy_screen * (np.arange(Ny)-Ny//2)


'''show aperture'''
# ax1.imshow(sheet.E, extent = [x_screen[0], 
#                         x_screen[-1] + dx_screen, 
#                         y_screen[0], 
#                         y_screen[-1] + dy_screen], 
#                         cmap ='gray', interpolation = "bilinear", aspect = 'auto')


'''show diffraction'''
ax1.imshow(abs_c, extent = [x_screen[0], 
                            x_screen[-1] + dx_screen, 
                            y_screen[0], 
                            y_screen[-1] + dy_screen], 
                            cmap ='gray', interpolation = "bilinear", aspect = 'auto')


ax2.plot(x_screen, abs_c[Ny//2]**2, linewidth = 1)

ax1.set_ylabel("y (mm)")
ax2.set_xlabel("x (mm)")
ax2.set_ylabel("Probability Density $|\psi|^{2}$")
ax1.set_xlim([-2,2])
ax2.set_xlim([-2,2])
ax1.set_ylim([-1,1])
plt.setp(ax1.get_xticklabels(), visible=False)


plt.show()
