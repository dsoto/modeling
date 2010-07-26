from __future__ import print_function
import matplotlib.pyplot as mpl
import numpy as np
import sys
sys.path.append('../../')
import taperedElasticaBeam as teb

##################################################################
# creates a beam and sets its properties (angle not included)
def initBeam():
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 80e-6          # length of taper (m) at Lt beam has zero thickness

    beam=teb.taperedElasticaBeam()
    beam.setBeamDimensions(E=E, t=t, w=w, L=L, Lt=Lt)

    return beam

##################################################################
# creates the figure and axes, returns a tuple (fig, ax)
def initFig():
    figHeight = 6
    figWidth = 6
    fig = mpl.figure()
    fig.set_figheight(figHeight)
    fig.set_figwidth(figWidth)

    ax = fig.add_axes([.15,.3, .7,.6])
    ax.grid()
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('Effective Stiffness (N/m)')

    return (fig, ax)

##################################################################
# takes the specified test load normal to the surface of the
# cantilever and translates it to a shear and normal load with
# respect to the beam.
def setLoads(beam, angle, force):
    normal = force * np.cos(angle)
    shear  = force * np.sin(angle)
    beam.setAxialLoad(axialLoad=normal)
    beam.setShearLoad(shearLoad=shear)

##################################################################
# calculates displacement at the tip of the beam, then uses that
# to find the change in length normal to the cantelever (dx).
# using the known force normal to the cantelever, k is calculated
# as though the beam were a linear spring.
def calculateStiffness(beam, angle, force):
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    xTipInitial = beam.L
    xTipFinal = beam.xTipDisplacement()
    yTipFinal = beam.yTipDisplacement()
    dx = (xTipInitial - xTipFinal) * np.cos(angle)
    dy = (yTipFinal) * np.sin(angle)
    k = force / (dx + dy)
    print(k)
    return k

##################################################################
# takes the stiffness (k from previous method) and plots it on the
# axes.
def plotPoint(stiffness, fig, ax, angle):
    ax.plot(angle, stiffness, 'kx')

def annotatePlot():
    annotation = []
    annotation.append('length    = ' + str(beam.L*scale) + ' microns')
    annotation.append('thickness = ' + str(beam.t*scale) + ' microns')
    annotation.append('width     = ' + str(beam.w*scale) + ' microns')
    annotation.append('modulus   = ' + str(beam.E/scale) + ' MPa')
    annotation.append('force     = ' + str(force*scale)  + ' uN')
    from datetime import datetime
    annotation.append('date      = '
                             +datetime.now().strftime('%d %b %Y - %H:%M'))
    import os
    annotation.append('script    = '+os.path.abspath(__file__))
    annotation = '\n'.join(annotation)
    xPos = 0.01
    yPos = 0.01
    import matplotlib.font_manager as mpf
    textFont = mpf.FontProperties()
    textFont.set_family('monospace')
    textFont.set_size(6)
    fig.text(xPos, yPos, annotation, fontproperties=textFont)
    print('')
    print(annotation)

##################################################################
# finds the effective stiffness of a tapered beam that is tilted
# at an angle with respect to the surface of a force cantilever.
# the effective stiffness is found for the direction normal to
# the surface of the cantelever by measuring the change in length
# in that direction. the specified test load is divided by this
# change in length to get the effective spring constant k.

force = 1e-6                            #test load in micronewtons
scale = 1e6
beam = initBeam()
fig, ax = initFig()

angleDeg = np.linspace(0,90,10)            #0 is perp to cantilever
angleRad = angleDeg*np.pi/180

for (ad,ar) in zip(angleDeg, angleRad):
    setLoads(beam=beam, angle=ar, force=force)
    stiffness = calculateStiffness(beam=beam, angle=ar, force=force)
    plotPoint(stiffness=stiffness, fig=fig, ax=ax, angle=ad)

annotatePlot()
fig.savefig('angleStiffness.pdf')
