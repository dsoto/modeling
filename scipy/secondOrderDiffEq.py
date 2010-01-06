#!/usr/bin/env python
'''
simple examples of ordinary differential equations using scipy
'''

import scipy as sp
import scipy.integrate as spint

# derivative function
# for a simple harmonic oscillator
# generically  - takes in two functions and returns their derivatives
# specifically - takes in the function and its first derivative
#              - returns first and second derivatives
def derivative(F, t):
    f0, f1 = F
    # assign derivatives
    d0 =  f1
    # second derivative is negative of function
    d1 = -f0
    # return derivative of f0 and f1
    return d0, d1

# initial conditions
# here i use initial conditions for sin()
# y0 - zeroth derivative of y
# y1 - first  derivative of y
y0 = 0
y1 = 1
initialCondition = [y0, y1]

mesh = sp.linspace(0,2*sp.pi,100)

answer = spint.odeint(derivative,
                      initialCondition,
                      mesh)

print answer
# split out the two functions
# answer is a two column by N row matrix
y0 = answer[:,0]
y1 = answer[:,1]

import matplotlib.pyplot as plt

figure = plt.figure()
axes = figure.add_subplot(111)
axes.plot(mesh,y0,label='y0')
axes.plot(mesh,y1,label='y1')
axes.legend()
#figure.show()
figure.savefig('secondOrderDiffEq.pdf',transparent=True)