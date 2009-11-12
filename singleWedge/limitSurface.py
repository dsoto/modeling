#!/usr/bin/env python
'''
this script attempts some primitive modeling of 
limit surface relating to the peel zone model
'''

import numpy as np

# i don't know why i chose theta, this should be shear force
theta = np.linspace(0, 90, 10)

lengthWedge = 1

# the length of contact should be linear with shear force
# for some reason i chose 1.5 exponent
lengthContact = 0.1 * (theta / 90.0) ** 1.5

# offset parabola
lengthPeel = 0.1*((theta - 30)/90.0)**2 + 0.01

import matplotlib.pyplot as mpl

figure = mpl.figure()

top = figure.add_subplot(211)
top.plot(lengthContact, -lengthPeel)
top.set_xlabel('Shear Force')
top.set_ylabel('Normal Force')

bot = figure.add_subplot(212)
bot.plot(theta,lengthContact, label='contact')
bot.plot(theta,lengthPeel, label='peel')
bot.set_xlabel('Parameter Variable')
bot.set_ylabel('Length')
bot.legend()

figure.set_figheight(8)
figure.set_figwidth(6)
figure.set_dpi(100)

figure.savefig('limitSurface.pdf', transparent=True)
#mpl.show()
