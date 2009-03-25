#!/usr/bin/env python
'''
create a visual representation of dalquist criterion
by simulating a fractalish surface and the deformation
of an adhesive material to that surface
'''

import numpy             as np
import numpy.random      as nr
import matplotlib.pyplot as mpl
import os

# seed random number generator

# number of frequency components
N = 50
# scaling exponent
p = 0.9
# top of plot
plotTop = 6
# plot separation between surfaces
plotSep = 2

# create vector of random phases
nr.seed(1)
phase = nr.rand(N)

# initialize data arrays
x = np.linspace(0,2*3.14,5000)
y = np.zeros((N+1,len(x)))
# offset surface from zero
y = y + 2

# create surface for each of i frequency components
for i in range(1,N+1):
    if i//2 == 1:
        y[i] = y[i-1] + 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i-1])
    else:
        y[i] = y[i-1] - 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i-1])

# generate plots
for i in range(N+1):
    fileName = 'plot' + '%02d'%(i) + '.png'
    print 'generating figure ' + fileName
    thisPlotSep = plotSep - (plotSep - 0.5) * i / N
    fig = mpl.figure()
    fig.set_size_inches((8,1.5))
    ax = fig.add_subplot(111)
    ax.fill_between(x, y[i]+thisPlotSep, plotTop, color = 'b')
    ax.fill_between(x, y[N-1], 0, color = 'r')
    ax.axis([0, 6, 0, plotTop])
    ax.set_axis_off()
    fig.savefig(fileName)
    mpl.close()
