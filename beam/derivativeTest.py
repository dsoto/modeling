#!/usr/bin/env python

import elasticaBeam as eb
import taperedElasticaBeam as teb
import scipy as sp
import matplotlib.pyplot as mpl


E = 2e6           # modulus of pdms
t = 19e-6           # thickness of beam
w = 19e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 52e-6           # length of beam
Lt = 100e-6         # length of taper

taperedBeam = teb.taperedElasticaBeam()
taperedBeam.setBeamDimensions(L,Lt,t,w,E)
load = 1e-5
taperedBeam.applyShearLoad(load)
taperedBeam.setNumPoints(20)
taperedBeam.printParameters()
taperedBeam.calculateSlopeFunction()
taperedBeam.calculateDisplacements()

beam = eb.elasticaBeam()
beam.setBeamDimensions(L,t,w,E)
load = 1e-5
beam.applyShearLoad(load)
beam.setNumPoints(20)
beam.printParameters()
beam.calculateEndAngle()
beam.calculateSlopeFunction()
beam.calculateDisplacements()

figure = mpl.figure()
ax = figure.add_subplot(111, aspect='equal')
taperedBeam.plotBeam(ax,'taperedBeam')
beam.plotBeam(ax,'untapered')
ax.legend()
mpl.show()

