#!/usr/bin/env python

'''
July 2, 2010 4:42:34 PM -0700

script to test strain energy computation in teb
'''

import matplotlib.pyplot as plt
import sys
import scipy as sp
sys.path.append('..')
import taperedElasticaBeam as teb

def configurePlot():
    width = 6.0                         # fig width
    height = 6.0                        # fig height
    fig = plt.figure()
    fig.set_figheight(height)
    fig.set_figwidth(width)
    ax = fig.add_axes((0.1,0.1,0.8,0.8))
    return fig, ax

def main():
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 1e6            # length of taper (m) at Lt beam has zero thickness

    # instantiate
    beam = teb.taperedElasticaBeam()
    beam.setBeamDimensions(L,Lt,t,w,E)

    shearLoad = sp.linspace(0,5e-6,11)
    energy = []

    for load in shearLoad:
        beam.setShearLoad(load)
        beam.calculateSlopeFunction()
        energy.append(beam.calculateStrainEnergy())

    fig, ax = configurePlot()
    ax.plot(shearLoad,energy)
    fig.savefig('energy.pdf')

    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 1e6            # length of taper (m) at Lt beam has zero thickness

    I = t**3 * w / 12.0

    beam = teb.taperedElasticaBeam()
    beam.setBeamDimensions(L,Lt,t,w,E)
    beam.setEndAngle(sp.pi/2)
    beam.calculateSlopeFunction()
    energy = beam.calculateStrainEnergy()
    print 'teb energy = ', energy

    analyticEnergy = (sp.pi/L/2.0)**2 * E * I / 2 * L
    print 'analytic energy = ',analyticEnergy

    energyError = (energy-analyticEnergy)/analyticEnergy
    print 'error as fraction =', energyError
