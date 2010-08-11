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
    height = 6.5                        # fig height
    fig = mpl.figure()
    fig.set_figheight(height)
    fig.set_figwidth(width)
    ax = fig.add_axes((0.2,0.2,0.7,0.55))
    ax.set_aspect('equal')
    ax.grid()
    return (fig, ax)

def calculateBeamDistance():
    loadGuess = -20
    correctLoad = fsolve(solveDist, loadGuess)
    print('Load = ', correctLoad, ' N')
    beam.plotBeam(fig[1], 'beam')

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

beam = teb.taperedElasticaBeam()
beam.setBeamDimensions(L=L, Lt=1, t=t, w=w, E=E)

fig = initFig()
calculateBeamDistance()
