#!/usr/bin/env python
'''
this script will eventually find the beam profile of a beam
for a given perpendicuar load at the end of the beam

December 21, 2009 1:15:16 PM -0800
today i want to add a displacement vs. shear load plot
as part of the output of this script

December 22, 2009 12:51:46 PM -0800
today i realized that this script currently finds the load
necessary to get a _given_ deflection.  i want to go the
other way which will involve numerically solving for the 
end slope for a _given_ load.  i need to make a function
that returns the length integral and use it to find a root.
'''

import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.integrate import trapz
from scipy           import sin
from scipy           import cos
from scipy           import sqrt
from scipy           import zeros
from scipy           import linspace
from scipy.optimize  import fsolve

E = 200e3           # modulus of pdms
t = 10e-6           # thickness of beam
w = 10e-6           # width of beam
I = t**3 * w / 12.0 # moment of inertia
L = 100e-6           # length of beam

debug = True 
#debug = False
# this function returns the normalized arc length of
# a beam using the arc length integral
def arcLengthIntegral(psiL):
    answer = quad(arcLengthElement,0,psiL,args=(psiL))[0]
    if (debug): 
        print 'normalized arc length = ',answer
        print 'psiL =', psiL
    return answer
    
# this function is used to provide the integrand
# for the normalized arc length
def arcLengthElement(psi,psiL):
    
    # how do i manage the singularity problem here during the solve routine?
    # if psiL is greater than pi/2, this will always return imaginary
    answer = 1/sqrt(sin(psiL)-sin(psi))
    # here my janky solution is to only take the real part
    #answer = answer.real
    answer = abs(answer)
    if (debug): 
        pass
        #print 'psi =',psi,'psiL =',psiL
        #print 'arcLengthElement =', answer
    return answer

# takes normalized arclength and multiplies by dimensions
# to scale to physical dimensions
def beamLength(psiL,load):
    #return arcLengthIntegral(psiL)
    answer = arcLengthIntegral(psiL) * sqrt(E*I/2/load)
    if (debug): print 'physical arc length = ',answer
    return answer

# compares computed beam length as a function of end slope
# to the measured beam length
def solveFunction(psiL, load):
    return L - beamLength(psiL,load)
    
nPts = 1
loadArray = linspace(.1,20,nPts) * 1e-6     # shear load on beam
loadArray = linspace(.1,.2,nPts) * 1e-6     # shear load on beam
loadArray = [.20*1e-6]
if (debug): print loadArray
#length = linspace(1,6,nPts)

#'''
# loop through values
angleGuess = 1.0
angle = zeros(nPts)
for i, thisLoad in enumerate(loadArray):
    angle[i] = fsolve(solveFunction, angleGuess, thisLoad)
    print thisLoad, angle[i]
    print '-'*50
#''' 

'''

realBeamLength = 6.8
ans = fsolve(solveFunction, angleGuess, realBeamLength)
print ans
'''
 
 
# here we find the load necessary for 
#load = (normalizedArcLength / L * sqrt(E * I / 2))**2 * 1e6
#load = normalizedArcLength
# get your plot on
'''
import matplotlib.pyplot as mpl
figure = mpl.figure()
ax = figure.add_subplot(111)
ax.plot(angleRange, load)
#ax.set_title('Load Required for End Slope $\psi_L$')
ax.set_title('Normalized Beam Length')
ax.set_xlabel('final slope ($\psi_L$)')
#ax.set_ylabel(r'shear load ($\mu$N)')
ax.set_ylabel(r'Normalized Beam Length ($L/L_0$)')
#ax.text(1,1,r'modulus\\thickness\\width\\length')
#ax.legend()
mpl.show()
'''