#!/usr/bin/env python
'''
integrate a curve of angle vs. arc length and plot
'''

import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.integrate import trapz
from scipy           import sin
from scipy           import cos
from scipy           import sqrt
from scipy           import zeros
from scipy           import linspace

# test to plot integral as function of variable
def arcLengthIntegral(psiL):
    return quad(arcLengthElement,0,psiL,args=(psiL))[0]
    
def arcLengthElement(psi,psiL):
    return 1/sqrt(sin(psiL)-sin(psi))
    
nPts = 100
angleRange = linspace(0.01,1.5,nPts)

arcLength = zeros(nPts)
for i,psiL in enumerate(angleRange):
#    print psiL
    arcLength[i] = arcLengthIntegral(psiL)
    
#print arcLength

# get your plot on
import matplotlib.pyplot as mpl
figure = mpl.figure()
ax = figure.add_subplot(111)
ax.plot(angleRange,arcLength)
ax.set_xlabel('final slope ($\psi_L$)')
ax.set_ylabel(r'arc length ($\sqrt{\frac{2P}{EI}}L$)')
#ax.legend()
mpl.show()
