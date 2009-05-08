#!/usr/bin/env python
'''
integrate a curve of angle vs. arc length and plot
'''

import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import trapz

# define derivative function for beam profile
def derivative(phi, s):
    return sp.sqrt(sp.sin(6*s**2))
    #return 2
    
initialCondition = 0

nPts = 1000
mesh = sp.linspace(0,1,nPts)

# solve ode to get slope function
answer = odeint(derivative, initialCondition, mesh)
# deal with silly mismatch between mesh dimensions and answer dimensions
answer = sp.transpose(answer)[0]

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
ax.plot(x, y, label='profile')
ax.set_xlabel('X')
ax.set_ylabel('Y')
#ax.legend()
mpl.show()
