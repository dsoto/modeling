#!/usr/bin/env python

from scipy.integrate import quad

# simple integration of linear function
def integrand(x):
    return x

start = 0
end = 1

# notice that x argument of integrand is implicit
(answer, errorEstimate) = quad(integrand, start, end) 
print answer

# now add slope and intercept of line
def integrand(x,m,b):
    return m*x + b

start = 0
end = 1

# notice that x argument of integrand is implicit
(answer, errorEstimate) = quad(integrand, start, end, args=(1,0)) 
print answer