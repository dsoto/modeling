from __future__ import print_function
import scipy as sp
import numpy as np
import matplotlib.pyplot as mpl
import sys
sys.path.append('../')
import taperedElasticaBeam as teb
from scipy.optimize import fsolve

def initFig():
    width = 6.5                         # fig width
    height = 9                          # fig height
    fig = mpl.figure()
    fig.set_figheight(height)
    fig.set_figwidth(width)
    ax1 = fig.add_axes((0.2,0.71,0.7,0.25))
    ax1.set_aspect('equal')
    ax1.grid()
    ax2 = fig.add_axes((0.2, 0.38, 0.7, 0.25))
#    ax2.set_aspect('equal')
    ax2.grid()
    ax3 = fig.add_axes((0.2, 0.05, 0.7, 0.25))
#    ax3.set_aspect('equal')
    ax3.grid()
    return (fig, ax1, ax2, ax3)

def calculateBeamDistance():
    loadGuess = -20
    correctLoad = fsolve(solveDist, loadGuess)
    print('Load          = ', correctLoad, ' N     neg=compression, pos=tension')
    strainEnergy = beam.calculateStrainEnergy()
    print('Strain Energy =  ', strainEnergy, ' J')
    jumpHeight = 2*strainEnergy/9.8/mass
    print('Jump Height   = ', jumpHeight, ' m     of pure, badass hops')
    beam.plotBeam(fig[1], 'beam')
    fig[1].plot(-beam.x, beam.y, color='b')
    beam.plotSlope(fig[2], 'slope')
    fig[2].plot(-beam.mesh, beam.slope, color='b')
    beam.plotCurvature(fig[3], 'curvature')
    fig[3].plot(-beam.mesh, beam.slopeDerivative, color='b')

def solveDist(load):
    beam.setAxialLoad(load)
    r = .1
    curvatureGuess = 1/r      # initial curvature bias to avoid a zero curvature solution
    beam.calculateSlopeFunction(curvatureGuess)
    beam.calculateDisplacements()
    d = 2*beam.xTipDisplacement()
    return d - arcDistance

E = 125e9               # elastic modulus of beam (Pa)
t = .001                # dimension of beam in bending direction (m)
w = .03                 # width of beam (m)
I = t**3 * w / 12.0     # moment of inertia for rectangular beam
L = .25                 # length of beam (m)
Lt = 1000               # length of taper (m) at Lt beam has zero thickness

arcDistance = .25       # desired distance between two ends of the beam
mass = .5               # mass in kg of whatever is jumping

beam = teb.taperedElasticaBeam()
beam.setBeamDimensions(L=L, Lt=1, t=t, w=w, E=E)

fig = initFig()
calculateBeamDistance()
