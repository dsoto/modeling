#!/usr/bin/env python

import sys
sys.path.append('../')
import elasticaBeam as eb
import scipy as sp

E = 2e6           # modulus of pdms
t = 20e-6           # thickness of beam
w = 20e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 50e-6           # length of beam

import matplotlib.pyplot as mpl
figure = mpl.figure()
#ax = figure.add_subplot(111)
ax = figure.add_axes((0.1,0.4,0.8,0.5))
startLoad = 1e-6
endLoad = 10e-6
loadArray = sp.linspace(startLoad, endLoad, 10)

beam = eb.elasticaBeam()
beam.setBeamDimensions(L,t,w,E)
beam.printParameters()

displacementArray = sp.zeros(10)

for i,load in enumerate(loadArray):
    beam.applyShearLoad(load)
    #beam.calculateEndAngle()
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.printResults()
    displacementArray[i] = beam.yDisplacement()
#    legendString = str(load)
#    beam.plotBeam(ax,legendString)

x = sp.linspace(0, endLoad,11)
eulerSpringConstant = E*w*t**3/L**3/4
y = 1 / eulerSpringConstant * x
ax.plot(loadArray*1e6,displacementArray*1e6,'o',label='elastica beam')
ax.plot(x*1e6,y*1e6,label = 'euler spring constant')
ax.set_xlabel(r'Shear Load ($\mu$N)')
ax.set_ylabel(r'Tip Displacement ($\mu$m)')
figure.suptitle('Elastica Beam and Euler Beam')
ax.set_xlim((0,10.5))
# axes.set_ylim((-0.1,1.1))


import os
from datetime import datetime
strings = [os.path.abspath(__file__),
           datetime.now().strftime('%Y-%m-%d %H:%M'),
           'load ='+str(load),
           'length ='+str(L),
           'thickness ='+str(t),
           'width ='+str(w),
           'modulus ='+str(E)]

yPos = -5
for thisString in strings:
    ax.text(0,yPos,thisString)
    yPos -= 0.9

#mpl.show()
figure.subplots_adjust(top=2)
figure.set_figheight(6)
figure.set_figwidth(6)

l = ax.legend(loc='best')
l.legendPatch.set_alpha(0.0)
figure.savefig('elasticaSpringConstant.pdf',transparent=True)
