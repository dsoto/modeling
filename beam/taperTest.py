#!/usr/bin/env python

import elasticaBeam as eb
import taperedElasticaBeam as teb
import scipy as sp
import matplotlib.pyplot as mpl
import os
from datetime import datetime


E = 2e6             # modulus of pdms
t = 20e-6           # thickness of beam
w = 20e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 50e-6           # length of beam
numPoints = 100

# loop through a set of taper lengths
Lt = [1,1e-4,75e-6,55e-6]
taperedBeam = teb.taperedElasticaBeam()
taperedBeam.setDebug(False)
load = 1e-5
taperedBeam.applyShearLoad(load)
taperedBeam.setNumPoints(numPoints)

# set up plot
figure = mpl.figure()
ax = figure.add_subplot(111, aspect='equal')

# loop and plot to axes object
for thisLt in Lt:
    taperedBeam.setBeamDimensions(L,thisLt,t,w,E)
    taperedBeam.calculateSlopeFunction()
    taperedBeam.calculateDisplacements()
    taperedBeam.plotBeam(ax,str(thisLt))

# plot untapered beam for comparison
beam = eb.elasticaBeam()
taperedBeam.setDebug(False)
beam.setBeamDimensions(L,t,w,E)
beam.applyShearLoad(load)
beam.setNumPoints(numPoints)
beam.calculateSlopeFunction()
beam.calculateDisplacements()
beam.plotBeam(ax,'untapered')

# annotate plot
ax.legend(loc='best')
ax.set_xlabel('X (microns)')
ax.set_ylabel('Y (microns)')
figure.suptitle('Beam Deflection Using Elastica Model')
yPos = -8
strings = [os.path.abspath(__file__), 
           datetime.now(),
           'load ='+str(load),
           'length ='+str(L),
           'thickness ='+str(t),
           'width ='+str(w)]

for thisString in strings:
    ax.text(0,yPos,thisString)
    yPos -= 2.0
#mpl.show()
figure.subplots_adjust(top=1)
figure.set_figheight(6)
figure.set_figwidth(6)
figure.savefig('taperTest.pdf',transparent=True)
 
