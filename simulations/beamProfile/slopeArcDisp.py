import matplotlib.pyplot as mpl
import numpy as np
import matplotlib.font_manager as font
from datetime import datetime
import os
import sys
sys.path.append('../../')
import taperedElasticaBeam as teb

############################################################################
# takes desired dimensions and loads for the beams and returns them
# as a dictionary
def setDimensions():
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 120e-6          # length of taper (m) at Lt beam has zero thickness

    shearLoad = 5e-6     # shear load
    endAngleDeg = 90     # end angle in degrees

    toRadians = np.pi/180
    endAngle = endAngleDeg*toRadians

    return ({'E':E, 't':t, 'w':w, 'L':L, 'Lt':Lt,
            'shearLoad':shearLoad, 'endAngleDeg':endAngleDeg,
            'endAngle':endAngle})

############################################################################
# takes dimension dictionary from setDimensions() and uses it to create
# taperedElasticaBeam objects. returns a tuple (tapered, untapered)
def initBeams(dim):
    tapered = teb.taperedElasticaBeam()
    tapered.setBeamDimensions(L=dim['L'], Lt=dim['Lt'], t=dim['t'],
                              w=dim['w'], E=dim['E'])
    tapered.setShearLoad(shearLoad=dim['shearLoad'])
    tapered.setEndAngle(endAngle=dim['endAngle'])

    untapered = teb.taperedElasticaBeam()
    untapered.setBeamDimensions(L=dim['L'], Lt=1, t=dim['t'],
                                w=dim['w'], E=dim['E'])
    untapered.setShearLoad(shearLoad=dim['shearLoad'])
    untapered.setEndAngle(endAngle=dim['endAngle'])

    return (tapered, untapered)

############################################################################
# takes a tuple of beams and initializes the figure and axes objects for
# the plot. returns a dictionary {'fig', 'axT1', 'axB1', 'axB2'} T is top,
# B is bottom.
def initFig(beams):

    figHeight = 9
    figWidth = 6.5
    fig = mpl.figure()
    fig.set_figwidth(figWidth)
    fig.set_figheight(figHeight)

    axHeight = .33
    axWidth = .33
    firstColumnLeft = (.5 - axWidth +.05)/2
    print firstColumnLeft
    secondColumnLeft = (.5 + axWidth + .3)/2
    bottom = .33

    axT1 = fig.add_axes([firstColumnLeft, bottom, axWidth, axHeight])
    axT1.set_aspect('equal')
    axT1.grid()
    axT1.set_xlabel('X', fontsize = 'small')
    axT1.set_ylabel('Displacement', fontsize = 'small')

    axB1 = fig.add_subplot(211)
    mpl.subplots_adjust(left=secondColumnLeft, bottom=bottom,
                    right=secondColumnLeft+axWidth, top=bottom+axHeight, hspace=.4)
    axB1.grid()
    axB1.set_xlabel('Arc Length', fontsize = 'small')
    axB1.set_ylabel('Slope', fontsize = 'small')

    axB2 = fig.add_subplot(212)
    axB2.grid()
    axB2.set_xlabel('Arc Length', fontsize = 'small')
    axB2.set_ylabel('Radius of Curvature (e-6)', fontsize = 'small')

    return {'fig':fig, 'axT1':axT1, 'axB1':axB1, 'axB2':axB2}

def plotDisp(beams, ax):
    scale = 1e6
    for i in beams:
        i.calculateSlopeFunction()
        i.calculateDisplacements()
        ax.plot(scale*i.x, scale*i.y)

def plotSlopeAndArc(beams, ax1, ax2):
    scale = 1e6
    x = np.linspace(0, beams[1].L, beams[1].numPoints)
    color = ('b', 'g')
    for i,j in zip(beams, color):
        ax1.plot(scale*x, i.slope*180/np.pi, j)
    for i,j in zip(beams, color):
        ax2.plot(scale*x, scale*1/abs(i.slopeDerivative), color=j, linestyle='-')
    plotFont = font.FontProperties()
    plotFont.set_size('small')
    mpl.legend(['tapered', 'untapered'], ncol = 2, bbox_to_anchor = (-.15, -.6, .5,.2))

def main():
    dimensions = setDimensions()
    beams = initBeams(dim=dimensions)
    fig = initFig(beams=beams)
    plotDisp(beams=beams, ax=fig['axT1'])
    plotSlopeAndArc(beams=beams, ax1=fig['axB1'], ax2=fig['axB2'])
    fig['fig'].savefig('test.pdf')
    addChartJunk(beams=beams)

main()