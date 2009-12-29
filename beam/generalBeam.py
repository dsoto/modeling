#!/usr/bin/env python
'''
integrate a curve of angle vs. arc length and plot
we define the derivative of the slope curve
and then integrate this function
the 
'''

import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import trapz

E = 2e6           # modulus of pdms
t = 19e-6           # thickness of beam
w = 19e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 52e-6           # length of beam

debug = True
'''
define function for the derivative of the 
slope of the beam profile
'''
psiL = 0.5604
def derivative(psi, s):
    if (debug): print psiL
    factor = sp.sqrt(2*1e-5/E/I)
    answer = sp.sqrt(sp.sin(psiL)-sp.sin(psi))
    return answer * factor
    
initialCondition = 0.0

nPts = 100
mesh = sp.linspace(0,L,nPts)

# solve ode to get slope function
answer = odeint(derivative, initialCondition, mesh)
# deal with silly mismatch between mesh dimensions and answer dimensions
answer = sp.transpose(answer)[0]
if (debug): print answer


# initialize position arrays
x = sp.zeros(nPts)
y = sp.zeros(nPts)


# take trig functions for position integrals
xInt = sp.cos(answer)
yInt = sp.sin(answer)

# loop through and numerically integrate discrete functions
for i,val in enumerate(mesh):
    x[i] = trapz(xInt[:i+1],mesh[:i+1])
    y[i] = trapz(yInt[:i+1],mesh[:i+1])

# get your plot on
import matplotlib.pyplot as mpl
figure = mpl.figure()
ax = figure.add_subplot(111, aspect='equal')
#ax = figure.add_subplot(111)
ax.plot(x, y, label='profile')
ax.set_xlabel('X')
ax.set_ylabel('Y')
#ax.legend()
mpl.show()
