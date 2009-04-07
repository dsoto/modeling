#!/usr/bin/env python

'''
7 April 2009 09:22:53 PDT
simple examples of root finding using scipy
'''

import scipy          as sp
import scipy.optimize as spop

# simple single variable function
def myfun(x):
    return x
    
guess = 1.0
ans = spop.fsolve(myfun,guess)
print ans

# now use function with two variables
def myfun(x,y):
    return x + y
    
guess = 1.0
secondArgument = 2.0
ans = spop.fsolve(myfun, guess, secondArgument)
print ans

# now solve for vector of y values
# could use list or array

guess = [0,0]
secondArgument = [0,1]
ans = spop.fsolve(myfun, guess, secondArgument)
print ans
