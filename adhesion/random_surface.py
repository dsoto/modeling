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

# number of frequency components
N = 50
# scaling exponent
p = 0.9
# top of plot
plotTop = 6
# plot separation between surfaces
plotSep = 2

# seed random number generator
nr.seed(1)
# create vector of random phases
phase = nr.rand(N)

# initialize data arrays
x = np.linspace(0,2*3.14,5000)
y = np.zeros((N+1,len(x)))
# offset surface from zero
y = y + 2
# initialize energy arrays

# create random adhesive and substrate surfaces
for i in range(1,N+1):
    # create surface from each of i frequency components
    # using series of sines with random phase
    if i//2 == 1:
        y[i] = y[i-1] + 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i-1])
    else:
        y[i] = y[i-1] - 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i-1])


# create data for energy balance
yMin = -3
yMax = 3
xMin = 0
xMax = 10
numPoints = 100
xEnergy = np.linspace(xMin, xMax, numPoints)
surfaceEnergy     = np.zeros((N+1,len(xEnergy)))
deformationEnergy = np.zeros((N+1,len(xEnergy)))
totalEnergy       = np.zeros((N+1,len(xEnergy)))
for i in range(N+1):
    # create plot for energy balance
    surfaceEnergy[i] = -0.3 * xEnergy
    deformationEnergy[i] = 0.5 * (N+1-i) / (N+1) * xEnergy**2
    totalEnergy[i] = surfaceEnergy[i] + deformationEnergy[i]

grey        = (0.5,0.5,0.5)
topColor    = (0.5,0.5,1.0)
bottomColor = (0.5, 0.5, 0.5)

# generate plots
for i in range(N+1):
    fileName = 'plot' + '%02d'%(i) + '.png'
    print 'generating figure ' + fileName
    thisPlotSep = plotSep - (plotSep - 0.5) * i / N
    fig = mpl.figure()
    fig.set_size_inches((6,4))
    # surface plot
    ax = fig.add_subplot(211)
    # deformed adhesive
    ax.fill_between(x, y[i]+thisPlotSep, plotTop, color = topColor)
    # rough substrate
    ax.fill_between(x, y[N-1], 0, color = bottomColor)
    ax.axis([0, 6, 0, plotTop])
    ax.set_axis_off()
    # energy plot
    ax = fig.add_subplot(212)
    ax.plot(xEnergy, surfaceEnergy[i],     
            label='Surface Energy',
            color='k')
    ax.plot(xEnergy, deformationEnergy[i], 
            label='Deformation Energy',
            color=topColor)
    ax.plot(xEnergy, totalEnergy[i],       
            label='Total Energy',
            color='green')
    # find min of total energy
    # plot grey line horizontal and vertical through min
    energyMinX = xEnergy[np.argmin(totalEnergy[i])]
    energyMinY = np.min(totalEnergy[i])
    plotMinX = np.linspace(xMin, xMax, numPoints)
    plotMinY = energyMinY * np.ones(numPoints)
    ax.plot(plotMinX, plotMinY, color=grey)
    plotVertX = energyMinX * np.ones(numPoints)
    plotVertY = np.linspace(yMin, yMax, numPoints)
    ax.plot(plotVertX, plotVertY, color=grey)
    ax.legend()
    ax.axis([xMin, xMax, yMin, yMax])
    ax.set_xlabel('Intimate Contact (arb units)')
    ax.set_ylabel('Energy (arb units)')
    fig.savefig(fileName)
    mpl.close()
