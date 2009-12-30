#!/usr/bin/env python

import elasticaBeam as eb
import scipy as sp

E = 2e6           # modulus of pdms
t = 19e-6           # thickness of beam
w = 19e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 52e-6           # length of beam

import matplotlib.pyplot as mpl
figure = mpl.figure()
ax = figure.add_subplot(111)

loadArray = sp.linspace(0.1e-6,1e-6,10)

beam = eb.elasticaBeam()
beam.setBeamDimensions(L,t,w,E)
beam.printParameters()

displacementArray = sp.zeros(10)

for i,load in enumerate(loadArray):
    beam.applyShearLoad(load)
    beam.calculateEndAngle()
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.printResults()
    displacementArray[i] = beam.yDisplacement()
#    legendString = str(load)
#    beam.plotBeam(ax,legendString)

x = sp.linspace(0,1,11)
y = 1 / 0.46 * x
ax.plot(loadArray*1e6,displacementArray*1e6,'o',label='elastica beam')
ax.plot(x,y,label = 'euler spring constant')
ax.set_xlabel(r'Shear Load ($\mu N$)')
ax.set_ylabel(r'Tip Displacement($\mu m$)')
l = ax.legend()
l.legendPatch.set_alpha(0.0)
figure.savefig('elasticaSpringConstant.pdf',transparent=True)
