#!/usr/bin/env python

import taperedElasticaBeam as teb
import matplotlib.pyplot   as plt

E = 2e6           # modulus of pdms
t = 19e-6           # thickness of beam
w = 19e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 52e-6           # length of beam
Lt = 60e-6         # length of taper
Lt = 1000000e-6         # length of taper

thisBeam = teb.taperedElasticaBeam()
thisBeam.setBeamDimensions(L,Lt,t,w,E)
load = 1e-5
thisBeam.applyShearLoad(load)
thisBeam.printParameters()
thisBeam.calculateSlopeFunction()
thisBeam.calculateDisplacements()

figure = plt.figure()
# figure size and resolution
width = 9
height = 9
figure.set_figheight(height)
figure.set_figwidth(width)

#ax = figure.add_subplot(121)
#ax = figure.add_axes((left_margin, height/2+0.5, 
#                      width-left_margin-right_margin, 1))
ax = figure.add_axes((0.1,0.6,0.8,0.35))
thisBeam.plotBeam(ax,'profile')
ax.legend(loc='best')

sw = 0.35
sh = 0.2
#ax = figure.add_subplot(322)
ax = figure.add_axes((0.1,0.3,sw,sh))
thisBeam.plotSlope(ax,'slope')
ax.legend(loc='best')

#ax = figure.add_subplot(324)
#ax = figure.add_axes((0.1+sw+0.1,0.1,sw,sh))
#thisBeam.plotCurvature(ax,'curvature')
#ax.legend(loc='best')

#ax = figure.add_subplot(326)
ax = figure.add_axes((0.1+sw+0.1,0.3,sw,sh))
thisBeam.plotRadiusOfCurvature(ax,'radius')
ax.legend(loc='best')

from datetime import datetime
import os
string  = ('load = '+str(load*1e6)+' microns'+'\n'+
           'length = '+str(L*1e6)+' microns'+'\n'+
           'thickness = '+str(t*1e6)+' microns'+'\n'+
           'width = '+str(w*1e6)+' microns'+'\n'+
           'modulus = '+str(E/1e6)+' MPa'+'\n'+
           'taper length = '+str(Lt*1e6)+' microns' +'\n'+
           datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
           os.path.abspath(__file__))

xPos = 0.5
yPos = 0.05
plt.figtext(xPos, yPos, string, fontsize = 10,ha='center')


figure.savefig('scratch.pdf',transparent=True)