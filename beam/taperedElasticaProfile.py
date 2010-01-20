#!/usr/bin/env python

import taperedElasticaBeam as teb
import scipy as sp

E = 2e6           # modulus of pdms
t = 20e-6           # thickness of beam
w = 20e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 50e-6           # length of beam
Lt = 55e-6          # length of taper

import matplotlib.pyplot as mpl
figure = mpl.figure()
ax = figure.add_axes((0.1,0.4,0.8,0.5))

loadArray = sp.linspace(0.1e-6,20e-6,10)

beam = teb.taperedElasticaBeam()
beam.setBeamDimensions(L,Lt,t,w,E)
beam.printParameters()

for i,load in enumerate(loadArray):
    beam.applyShearLoad(load)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.printResults()
    legendString = str('%5.2e' % load) 
    beam.plotBeam(ax,legendString)

ax.set_xlabel(r'x Displacement ($\mu$m)')
ax.set_ylabel(r'y Displacement ($\mu$m)')
l = ax.legend(loc='best')

# figure size and resolution
width = 6
height = 6
figure.set_figheight(height)
figure.set_figwidth(width)

import os
from datetime import datetime
xPos = 0.5
yPos = 0.05
strings = [os.path.abspath(__file__), 
           datetime.now().strftime('%d %b %Y - %H:%M'),
           'load = '+str(load*1e6)+' microns',
           'length = '+str(L*1e6)+' microns',
           'thickness = '+str(t*1e6)+' microns',
           'width = '+str(w*1e6)+' microns',
           'modulus = '+str(E/1e6)+' MPa']

strings = ['length = '+str(L*1e6)+' microns'+'\n'+
           'taper length ='+str(Lt*1e6)+' microns'+'\n'+
           'thickness = '+str(t*1e6)+' microns'+'\n'+
           'width = '+str(w*1e6)+' microns'+'\n'+
           'modulus = '+str(E/1e6)+' MPa'+'\n'+
           datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
           os.path.abspath(__file__)]

for thisString in strings:
    mpl.figtext(xPos, yPos, thisString, fontsize = 10,ha='center')
    yPos -= 0.03
'''
'''




l.legendPatch.set_alpha(0.0)
figure.savefig('taperedElasticaProfile.pdf',transparent=True)
