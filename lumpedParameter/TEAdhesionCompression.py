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

l = 200    # in microns
kt = .1    # in newton * meter
ks = 1     # in newton / meter

maxDisplacementShear = 1
numPoints = 101
displacementShear = sp.linspace(0,maxDisplacementShear,numPoints)
ds = displacementShear

def surface(y,x):
    return y - sp.sqrt(1 - x**2)

'''
dnList = []
for point in ds:
    dnGuess = 1-point
    dn = spop.fsolve(surface,dnGuess,point)
    print dn
    dnList.append(dn)

dnList = sp.array(dn)
'''
dnGuess = 1-ds
dn = spop.fsolve(surface,dnGuess,ds)

plt.plot(ds,dn)
plt.show()

# equation of dn vs. ds for zero normal force
# should i not use ds as a vector for the fzero routine?
# or should all the other quantities by vectors of the same dimension 
# if i use this approach?

# lf = sqrt(ds.^2+(l-dn).^2);
#fn = inline('kt*ds*asin(ds/sqrt(ds^2+(l-dn)^2)) / sqrt(ds^2+(l-dn)^2)^2 - ks*(sqrt(ds^2+(l-dn)^2)-l)*(l-dn)/sqrt(ds^2+(l-dn)^2)','dn','ds','ks','kt','l');
#z = fzero(fn,[0,200],ds,ks,kt,l)


#dn = l - kt/ks.*asin(ds/lf).*ds/lf/(lf-l)

