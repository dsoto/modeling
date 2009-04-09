#!/usr/bin/env python

'''
8 April 2009 09:49:27 PDT
creating model of TE lumped parameter model to create 
a surface of compression vs adhesion in the displacement space
'''

import scipy             as sp
import scipy.optimize    as spop
import numpy             as np
import matplotlib.pyplot as plt

# dimensions and spring constants of structure
l = 200.0    # in microns
kt = 0.1     # in newton * meter
ks = 1.0     # in newton / meter

# create data grid to plot dn vs. ds
maxDisplacementShear = 100.0
numPoints = 11
displacementShear = sp.linspace(0.0,maxDisplacementShear,numPoints)
ds = displacementShear
dn = sp.zeros(numPoints)

# calculate length of spring in model
def calclf(dn, ds, l):
    return sp.sqrt(ds**2 + dn**2 + l**2 - 2*dn*l)

# calculate normal force at interface
def normalForce(dn, ds, ks, kt, l):
    lf = calclf(dn, ds, l)
    return ((kt * ds * sp.arcsin(ds/lf))/lf**2
            - (ks*(lf-l)*(l-dn))/lf)

# loop through shear displacement values and find
# normal displacement that results in zero normal force
for i, point in enumerate(ds):
    dnGuess = point
    dnGuess = 100
    dn[i] = spop.fsolve(normalForce, dnGuess, (point, ks, kt, l))

figure = plt.figure()
figure.suptitle('Adhesion vs. Compression\nTE Lumped Parameter Model\nl = 200\nkt = 0.1\nks = 1.0')

axes = figure.add_subplot(111)
axes.plot(ds,dn)
axes.set_xlabel(r'Shear Displacment $(\mu m)$')
axes.set_ylabel(r'Normal Displacment $(\mu m)$')

figure.savefig('AdhesionVsCompression.pdf',transparent=True)
plt.show()


