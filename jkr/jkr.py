#!/usr/bin/env python
'''
2D plot of JKR adhesion for microwedge tip
'''

import numpy as np

pi = 3.1415
gamma = 0.05

R = np.linspace(1,10,11)

adhesion = 3*pi/2*R*gamma

import matplotlib.pyplot as mpl

figure = mpl.figure()
ax = figure.add_subplot(111)
ax.plot(R, adhesion, label='adhesion')
ax.set_xlabel('Radius (um)')
ax.set_ylabel('Pulloff force (uN)')
ax.legend()
mpl.show()
