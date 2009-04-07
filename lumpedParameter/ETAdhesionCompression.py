#!/usr/bin/env python

# lumped parameter modeling for adhesion vs compression
# April 3, 2008 9:18:16 AM PDT

# 24 July 2008 16:38:12 PDT
# this model will map out the adhesive vs. compressive areas of the TE
# lumped parameter model in the shear vs. normal displacement space

# 7 April 2009 08:48:49 PDT
# porting model to python / scipy

import scipy             as sp
import scipy.optimize    as spop
import matplotlib.pyplot as plt

l = 200.0    # in microns
kt = 0.1     # in newton * meter
ks = 1.0     # in newton / meter

maxDisplacementShear = 100.0
numPoints = 11
displacementShear = sp.linspace(0.0,maxDisplacementShear,numPoints)
ds = displacementShear

def surface(dn, ds, ks, kt, l):
    rhs = (- kt * ds * sp.arcsin(ds/l) / ks / l**2
           - sp.sqrt(l**2 - ds**2) + l)
    return dn - rhs

dn = sp.zeros(numPoints)
for i, point in enumerate(ds):
    dnGuess = point
    dn[i] = spop.fsolve(surface, dnGuess, (point, ks, kt, l))

plt.plot(ds,dn)
plt.show()