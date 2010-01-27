#!/usr/bin/env python

import elasticaBeam as eb
import taperedElasticaBeam as teb
import scipy as sp
import matplotlib.pyplot as mpl


E = 2e6             # modulus of pdms
t = 20e-6           # thickness of beam
w = 20e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 50e-6           # length of beam
Lt = 1000000e-6         # length of taper
numPoints = 100


taperedBeam = teb.taperedElasticaBeam()
taperedBeam.setDebug(False)
taperedBeam.setBeamDimensions(L,Lt,t,w,E)
load = 1e-5
taperedBeam.applyShearLoad(load)
taperedBeam.setNumPoints(numPoints)
taperedBeam.printParameters()
taperedBeam.calculateSlopeFunction()
taperedBeam.calculateDisplacements()

beam = eb.elasticaBeam()
taperedBeam.setDebug(False)
beam.setBeamDimensions(L,t,w,E)
load = 1e-5
beam.applyShearLoad(load)
beam.setNumPoints(numPoints)
beam.printParameters()
beam.calculateSlopeFunction()
beam.calculateDisplacements()

figure = mpl.figure()
ax = figure.add_subplot(111, aspect='equal')
taperedBeam.plotBeam(ax,'taperedBeam')
beam.plotBeam(ax,'untapered')
ax.legend(loc='best')
mpl.show()

