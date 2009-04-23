#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as mpl
import os

mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
mpl.rcParams['axes.labelsize']  = 18
mpl.rcParams['figure.figsize'] = (6, 4)
#mpl.rcParams['figure.subplot.left'] = 0.9
#mpl.rcParams['figure.subplot.right'] = 1.0

xStart = 3
xEnd = 8
x = np.linspace(xStart,xEnd,500)
depth = 90*0.0001239
sigma = 3.4
y = 4*depth*((sigma/x)**12 - (sigma/x)**6)

figure = mpl.figure()
axes = figure.add_axes([0.2, 0.2, 0.7, 0.7])
grey = (0.5,1.0,1.0)
axes.plot(x,y,color=grey)
axes.axis([xStart, xEnd, -0.02, 0.05])
axes.set_xlabel(r'Distance (\AA)')
axes.set_ylabel('Interaction Energy (eV)')
#figure.suptitle('Energy for Argon Dimer')
figure.savefig('lennardJones.pdf',transparent=True)
os.system('open lennardJones.pdf')