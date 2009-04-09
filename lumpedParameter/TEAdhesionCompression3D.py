#!/usr/bin/env python

'''
8 April 2009 09:49:27 PDT
creating model of TE lumped parameter model to create 
a surface of compression vs adhesion in the displacement space

9 April 2009 11:12:28 PDT
altered to provide 3D surface plotting of the normal force
at the adhesive interface
'''

import scipy             as sp
import scipy.optimize    as spop
import numpy             as np
import matplotlib.pyplot as plt

l = 200.0    # in microns
kt = 0.1     # in newton * meter
ks = 1.0     # in newton / meter

maxDisplacementShear = 100.0
numPoints = 11
displacementShear = sp.linspace(0.0,maxDisplacementShear,numPoints)
ds = displacementShear

def calclf(dn, ds, l):
    return sp.sqrt(ds**2 + dn**2 + l**2 - 2*dn*l)

def normalForce(dn, ds, ks, kt, l):
    lf = calclf(dn, ds, l)
    return ((kt * ds * sp.arcsin(ds/lf))/lf**2
            - (ks*(lf-l)*(l-dn))/lf)


# 3D plotting of surface
import enthought.mayavi.mlab as mlab
[ds,dn] = np.mgrid[0:maxDisplacementShear+10:10,0:maxDisplacementShear+10:10]
f = normalForce(dn, ds, ks, kt, l)

s = mlab.surf(ds,dn,f)
mlab.axes(x_axis_visibility=True)
mlab.axes(y_axis_visibility=True)
mlab.axes(z_axis_visibility=True)
mlab.axes(xlabel='shear displacement')
mlab.axes(ylabel='normal displacement')
mlab.axes(zlabel='normal force')
mlab.show()

# how do i add an x-y plane?
