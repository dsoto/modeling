#!/usr/bin/env python
'''
2D plot of JKR adhesion for microwedge tip
'''

import numpy as np

pi = 3.1415
gamma = 0.05

R1 = np.linspace(1,10,11)
R2 = [10, 20, 30, 40, 50]

adhesion = np.zeros((len(R2),len(R1)))

import matplotlib.pyplot as mpl

figure = mpl.figure()
axes = figure.add_subplot(111)

for i, val in enumerate(R2):
    adhesion[i] = 3.0*pi/2.0*(R1*val)**(0.5)*gamma
    axes.plot(R1, adhesion[i], label=str(val)+r'$\mu$m')

axes.set_xlabel(r'Radius ($\mu$m)')
axes.set_ylabel(r'Pulloff force ($\mu$N)')
axes.grid(True,color=((0.5,0.5,0.5)))
axes.legend()
mpl.show()
