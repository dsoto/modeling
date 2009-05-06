#!/usr/bin/env python
'''
simple examples of ordinary differential equations using scipy
'''

import scipy as sp
import scipy.integrate as spint

# derivative function
def derivative(y,x):
    return y*x

initialCondition = 1

mesh = sp.linspace(0,1,10)

# why don't we need derivative(y,x) here
# is this implicitly specified somewhere?
answer = spint.odeint(derivative,
                      initialCondition,
                      mesh)

import matplotlib.pyplot as plt

figure = plt.figure()
axes = figure.add_subplot(111)
axes.plot(mesh,answer)
#figure.show()
figure.savefig('diffEq.pdf',transparent=True)
