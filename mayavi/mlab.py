#!/usr/bin/env python
'''
9 April 2009 11:15:32 PDT
creates a simple paraboloid and plots using 
mayavi.mlab 
'''

import numpy as np

# plotting ranges
start = -1
end = 1
dx = 0.1

# construct grid and surface
[x,y] = np.mgrid[start:end+dx:dx,start:end+dx:dx]
z = x**2 + y**2

# plot 
import enthought.mayavi.mlab as mlab
# first paraboloid
s1 = mlab.surf(x,y,z)
# second paraboloid to demonstrate multiple surfaces
s2 = mlab.surf(x,y,-z+1)
# open gui and show
mlab.show()