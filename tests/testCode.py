#!/usr/bin/env python

import sys
sys.path.append('../')
import taperedElasticaBeam as teb
import numpy as np
import scipy as sp
import matplotlib.pyplot as mpl
import matplotlib.font_manager as font
from datetime import datetime
import os

#########################################################
# creates a tuple of one untapered and one tapered beam.
def createBeams(E, t, w, I, L, Lt):
    untaperedBeam = teb.taperedElasticaBeam()
    taperedBeam = teb.taperedElasticaBeam()
    taperedBeam.setBeamDimensions(L=L, Lt=Lt, t=t, w=w, E=E)
    untaperedBeam.setBeamDimensions(L=L, Lt=1, t=t, w=w, E=E)
    return (untaperedBeam, taperedBeam)

#########################################################
# returns a tuple of a figure and the figure's axes.
def createFigure():
    width = 6.5                         # fig width
    height = 6.5                        # fig height
    fig = mpl.figure()
    fig.set_figheight(height)
    fig.set_figwidth(width)
    ax = fig.add_axes((0.1,0.3,0.8,0.55))
    ax.set_aspect('equal')
    ax.grid()
    return (fig, ax)

#########################################################
# calls the elastica test for both beams and euler for
# the untapered beam.
def test(beams, condition, conditionValue, figure):
    elastica(beams, condition, conditionValue, figure)
    euler(beams[0], condition, conditionValue, figure)

#########################################################
# solves elastica model for untapered and tapered beams
# and for either pointLoad or endAngle conditions
# by calling the solve functions from taperedElasticaBeam
# class.
def elastica(beams, condition, conditionValue, figure):
    if condition == 'endAngle':
        shearLoad = 0
        endAngle = conditionValue
    elif condition == 'pointLoad':
        shearLoad = conditionValue
        endAngle = 0
    for i in beams:
        i.setEndAngle(endAngle)
        i.setShearLoad(shearLoad)
        i.calculateSlopeFunction()
        i.calculateDisplacements()
        #NOTE: the legend string is overwritten later
        i.plotBeam(figure[1], 'elastica')

#########################################################
# solves euler model for untapered beam using either a
# point load at the tip of the beam or a point moment at
# the end of the beam.
def euler(utb, condition, conditionValue, figure):
    x = np.linspace(0, utb.L, utb.numPoints)
    if condition == 'pointLoad':
        p = conditionValue
        displacement = ((-p/(6*utb.E*utb.I))
                        * (x**3 - 3*utb.L*x**2))
    elif condition == 'endAngle':
        theta = conditionValue
        M = theta*utb.E*utb.I / utb.L
        displacement = M*x**2 / (2*utb.E*utb.I)
    scale = 10e5
    figure[1].plot(x*scale, displacement*scale, label = 'euler')

#########################################################
# adds legend to plot, text at bottom of the plot, saves
# the plot as a pdf with a timestamp.
def addChartJunk(tb, figure, condition):
    plotFont = font.FontProperties()
    plotFont.set_size('small')
    dateString = datetime.now().strftime('%d %b %Y - %H:%M')
    dateCode = datetime.now().strftime('%Y%m%d%H%M')
    string  = ('length = '+str(tb.L*1e6)+' microns'+'\n'+
               'thickness = '+str(tb.t*1e6)+' microns'+'\n'+
               'width = '+str(tb.w*1e6)+' microns'+'\n'+
               'modulus = '+str(tb.E/1e6)+' MPa'+'\n'+
               dateString+'\n' + os.path.abspath(__file__))
    xPos = 0.5
    yPos = 0.05
    mpl.figtext(xPos, yPos, string,
                ha='center')
    if condition[0] == 'endAngle':
        mpl.title('End Angle = ' + str(condition[1]*180/np.pi) + ' Degrees')
    elif condition[0] == 'pointLoad':
        mpl.title('Point Load = ' + str(condition[1]*1e6) + ' Micronewtons')

    # sets location of legend outside the axes using bbox_to_anchor arg.
    # the cordinates seem to be based off of the axes; if you make the bottom
    # equal to 0 i.e. (.8, 0), the top of the legend Bbox will be right on
    # the x axis. i can't figure out how to get the legend centered, but .8
    # seems about right for the 6.5 by 6.5 figures.
    figure[1].legend(['elastica: untapered', 'elastica: ' +
                      'taper length = '+str(int(tb.Lt*1e6))+' microns', 'euler: untapered'],
                       prop=plotFont, bbox_to_anchor = (.8, -.5))
    plotFileName = condition[0] + 'Plot-' + dateCode + '.pdf'
    figure[0].savefig(plotFileName, transparent=True)

#########################################################
# main: defines constants, desired point load and end angle.
# creates two plots (point load and end angle) with three
# models a piece (elastica model for the tapered and untapered
# beams, and an euler model for the untapered beam. Note
# that the euler model is only valid for small angles of
# deflection.
def main():
    E = 1e9              # elastic modulus of beam (Pa)
    t = .003            # dimension of beam in bending direction (m)
    w = .1            # width of beam (m)
    I = t**3 * w / 12.0  # moment of inertia for rectangular beam
    L = .25            # length of beam (m)
    Lt = 1000          # length of taper (m) at Lt beam has zero thickness

    endAngle = np.pi/8   # end angle condition
    pointLoad = 10     # point load condition

    endAngleTuple = ('endAngle', endAngle)
    pointLoadTuple = ('pointLoad', pointLoad)

    twoTests = (endAngleTuple, pointLoadTuple)

    for i in twoTests:
        condition = i

        # tuple of beams (untaperedBeam, taperedBeam)
        beams = createBeams(E=E, t=t, w=w, I=I, L=L, Lt=Lt)

        # tuple of figure and axes objects (fig, ax)
        figure = createFigure()

        # run either pointLoad test or endAngle test, depending on condition
        test(beams = beams, condition = condition[0], conditionValue = condition[1], figure = figure)

        # passes the tapered beam
        addChartJunk(tb = beams[1], figure = figure, condition = condition)

#########################################################
if __name__ == "__main__":
    main()