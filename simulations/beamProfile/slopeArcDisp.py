import matplotlib.pyplot as mpl
import matplotlib.font_manager as mpf
import numpy as np
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
    Lt = 80e-6          # length of taper (m) at Lt beam has zero thickness

    shearLoad = 2e-6     # shear load
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
    figWidth = 6.0
    fig = mpl.figure()
    fig.set_figwidth(figWidth)
    fig.set_figheight(figHeight)

    # NOTE: axHeight is just a nominal value used in positioning the two
    # subplots in the figure. The actual height of the top plot changes
    # when the beam displacement is plotted, so it isn't actually .33
    axHeight = .33
    axHeight = .35
    axWidth = (figHeight*axHeight)/figWidth
    axWidth = .7
    axLeft = (1 - axWidth)/2
    axT1Bottom = 1 - axHeight - .05

    #axT1 = fig.add_subplot(211)
    #axT1.set_position([axLeft, axT1Bottom, axWidth, axHeight])
    axT1 = fig.add_axes((axLeft, axT1Bottom, axWidth, axHeight))
    axT1.set_aspect('equal')
    axT1.grid()
    axT1.set_xlabel('X (um)')
    axT1.set_ylabel('Y (um)')
    axT1.set_title('Displacement')

    # NOTE: to set the height of the bottom subplot, you have to run the program,
    # look at the graph, and figure out what the ratio is. For the 90 deg end
    # angle, it was 4/5.
    #axB1 = fig.add_subplot(212)
    #axB1.set_position((axLeft, axT1Bottom - .1 - axHeight, axWidth, axHeight))
    axB1 = fig.add_axes((axLeft, axT1Bottom - .1 - axHeight, axWidth, axHeight))
    axB1.grid()
    axB1.set_xlabel('Arc Length (um)')
    axB1.set_ylabel('Slope (deg)')
    axB1.set_title('Slope and Curvature along Beam')

    axB2 = axB1.twinx()
    axB2.set_ylabel('Radius of Curvature (um)')

    return {'fig':fig, 'axT1':axT1, 'axB1':axB1, 'axB2':axB2}

############################################################################
# plots the beam displacement in the top plot. takes a list of beams and
# the top axis.
def plotDisp(beams, ax):
    scale = 1e6
    for i in beams:
        i.calculateSlopeFunction()
        i.calculateDisplacements()
        ax.plot(scale*i.x, scale*i.y)
    ax.legend(['tapered', 'untapered'], loc='best')

############################################################################
# plots the beam slope and arc vs position along the beam on the bottom
# figure. takes a list of beams and two axes for the bottom plot. the two
# axes objects share their x axis. Also adds a legend to bottom plot.
def plotSlopeAndArc(beams, ax1, ax2,fig):
    scale = 1e6
    x = np.linspace(0, beams[1].L, beams[1].numPoints)
    color = ('b', 'g')
    plotList = []
    stringList = []
    for i,j in zip(beams, color):
        plotList.append(ax1.plot(scale*x, i.slope*180/np.pi, j))
        stringList.append(str(i.Lt)+' slope')
    for i,j in zip(beams, color):
        plotList.append(ax2.plot(scale*x, scale*1/abs(i.slopeDerivative),
                                color=j, linestyle='--'))
        stringList.append(str(i.Lt)+' curvature')
    ax1.set_ylim((0,90))
    left   =  0.00
    bottom =  1.00 - 0.01
    width  =  0.90
    height =  0.10
    ax1.legend(plotList, stringList,
               bbox_to_anchor=[left, bottom, width, height],
               loc=3, ncol=2, mode='expand', prop={'size':10})

    # bbox_to_anchor sets the position of the legend w respect to axes object
    ax1.legend(plotList, stringList, prop={'size':10},
               bbox_to_anchor = [.1,.1,1,0],
               bbox_transform = fig['fig'].transFigure,
               ncol=2, loc=3)

############################################################################
# adds annotation at the bottom of the figure using Dan's fancy new method.
def addChartJunk(fig, beams):
    annotationStrings = []
    annotationStrings.append('length    = '+str(beams[1].L*1e6)+' microns')
    annotationStrings.append('thickness = '+str(beams[1].t*1e6)+' microns')
    annotationStrings.append('width     = '+str(beams[1].w*1e6)+' microns')
    annotationStrings.append('modulus   = '+str(beams[1].E/1e6)+' MPa')
    annotationStrings.append('date      = '
                             +datetime.now().strftime('%d %b %Y - %H:%M'))
    annotationStrings.append('script    = '+os.path.abspath(__file__))

    string = '\n'.join(annotationStrings)

    xPos = 0.01
    yPos = 0.01
    textFont = mpf.FontProperties()
    textFont.set_family('monospace')
    textFont.set_size(8)
    fig.text(xPos, yPos, string, fontproperties=textFont)

############################################################################
# creates beams, initializes beams, creates the plots, and saves plots as
# a pdf.
def main():
    dimensions = setDimensions()
    beams = initBeams(dim=dimensions)
    fig = initFig(beams=beams)
    plotDisp(beams=beams, ax=fig['axT1'])
    plotSlopeAndArc(beams=beams, ax1=fig['axB1'], ax2=fig['axB2'],fig=fig)
    addChartJunk(fig=fig['fig'],beams=beams)
    fig['fig'].savefig('test.pdf')

main()