#!/usr/bin/env python

'''
July 1, 2010 11:41:16 AM -0700

this will test a beam with a given shear load
and end angle
and then sweep the axial load and plot the
resulting deflections
'''
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import taperedElasticaBeam as teb

def main():
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 1e6            # length of taper (m) at Lt beam has zero thickness

    # instantiate
    beam = teb.taperedElasticaBeam()
    beam.setBeamDimensions(L,Lt,t,w,E)

    shearLoad = 1e-6     # point load condition
    endAngle = 3.1415/2
    axialLoad = [-2.0e-6, 0.0, 2.0e-6]
    beam.setShearLoad(shearLoad)
    beam.setEndAngle(endAngle)
    width = 6.0                         # fig width
    height = 6.0                        # fig height
    fig = plt.figure()
    fig.set_figheight(height)
    fig.set_figwidth(width)
    ax = fig.add_axes((0.1,0.1,0.8,0.8))
    #ax.set_aspect('equal')
    ax.grid()


    for al in axialLoad:
        beam.setAxialLoad(al)

        # solve psi(s) function
        beam.calculateSlopeFunction()

        # convert psi(s) to cartesian
        beam.calculateDisplacements()

        legendString = str(al)
        # plot beam position
        beam.plotBeam(ax,legendString)

    ax.legend(loc='best')
    fig.savefig('arbLoad.pdf')