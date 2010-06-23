#!/usr/bin/env python

#from __future__ import print_function
#from __future__ import division

import elasticaBeam        as eb
import taperedElasticaBeam as teb
import scipy               as sp

E = 2e6             # modulus of pdms
t = 20.9e-6           # thickness of beam at base
w = 24.3e-6           # width of beam at base
I = t**3 * w / 12.0 # moment of inertia
L = 50.0e-6           # length of beam

import matplotlib.pyplot as plt
figure = plt.figure()
ax = figure.add_axes((0.1,0.4,0.8,0.5))

# choose load for spring constant measurement
# since this is non-linear, it matters what load
load = 1e-6

# instantiate beams
beam = eb.elasticaBeam()
tbeam = teb.taperedElasticaBeam()

# loop over thicknesses
thicknessRange = sp.linspace(5e-6,25e-6,5)
springConstant = []
taperedSpringConstant = []
for t1 in thicknessRange:
    beam.setBeamDimensions(L,t1,w,E)
    # convert t1 to a taper that results in a thickness
    # t1 at the tip
    # see lab book 2009-1-55
    taper = t*L/(t-t1)
    # print(taper)
    tbeam.setBeamDimensions(L,taper,t,w,E)

    # apply loads and calculate beam
    beam.applyShearLoad(load)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()

    tbeam.debug = False
    tbeam.applyShearLoad(load)
    tbeam.calculateSlopeFunctionForPointLoad()
    tbeam.lengthInContact = 0
    tbeam.calculateDisplacements()

    springConstant.append(load / beam.yDisplacement())
    taperedSpringConstant.append(load / tbeam.yTipDisplacement())

for sc in (springConstant, taperedSpringConstant):
    print(sc)



ax.plot(thicknessRange*1e6,springConstant,label='beam')
ax.plot(thicknessRange*1e6,taperedSpringConstant,label='tapered beam')
ax.set_xlabel(r'Tip Thickness ($\mu$m)')
ax.set_ylabel(r'Lateral Spring Constant (N/m)')
ax.grid()
figure.suptitle('Spring Constant of Tapered and Untapered Beam')

#figure.subplots_adjust(top=2)
figure.set_figheight(6)
figure.set_figwidth(6)

import os
from datetime import datetime
dateNow = datetime.now()
dateString = dateNow.strftime('%Y-%m-%d %H:%M:%S')
fileDateString = dateNow.strftime('%Y%m%d-%H%M%S')
strings = []
strings.append(os.path.abspath(__file__))
strings.append(dateString)
strings.append(fileDateString+'.pdf')
strings.append('load = ' + str(load))
strings.append('length = ' + str(L))
strings.append('thickness = ' + str(t))
strings.append('width = ' + str(w))
strings.append('modulus = ' + str(E))
string = '\n'.join(strings)

xPos = 0.5
yPos = 0.05
plt.figtext(xPos, yPos, string,
            ha='center')

#plt.show()
l = ax.legend(loc='best')
l.legendPatch.set_alpha(0.0)
figure.savefig(fileDateString+'.pdf',transparent=True)

