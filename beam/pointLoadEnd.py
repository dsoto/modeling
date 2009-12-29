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

December 23, 2009 7:02:25 PM -0800
when i come back next time, i need to figure out the ODE solution

December 28, 2009 4:02:49 PM -0800
i have the end beam angle as a function of load
now i want to integrate the solution to find the profiles

December 29, 2009 11:27:22 AM -0800
this script along with generalBeam.py are giving me a consistent
looking solution for the beam profile.
my plan now is to create a beam object to facilitate repeated 
computation of profiles.
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
import matplotlib.pyplot as mpl
        
class beam:
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    I = t**3 * w / 12.0  # moment of inertia for rectangular beam
    L = 60e-6            # length of beam (m)
    numPoints = 100      # number of grid points for ODE
    debug = False
    shearLoad = 1e-6     # transverse load on beam (N)
    psiL = 0             # angle at end of beam (radians)

    def __init__(self):
        pass
        
    def setBeamDimensions(self, L, t, w, E):
        self.L = L
        self.t = t
        self.w = w
        self.E = E
        self.I = t**3 * w / 12.0
        
    def setNumPoints(self, numPoints):
        self.numPoints = numPoints
        
    def applyShearLoad(self, shearLoad):
        self.shearLoad = shearLoad
        
    def calculateEndAngle(self):
        angleTry = linspace(1e-9, 3.1415/2, 200)
        #try brute force solution to avoid problem with imaginary integrand
        for thisAngle in angleTry:
            error = self.L - self.beamLength(thisAngle, self.shearLoad)
            if (error < 0) :
                self.psiL = thisAngle
                if (self.debug): 
                    print 'final angle =',self.psiL
                    print '-'*50
                    print self.shearLoad, self.psiL
                break

    def calculateSlopeFunction(self):
        initialCondition = 0.0
        mesh = sp.linspace(0, self.L, self.numPoints)
        answer = odeint(self.derivative, initialCondition, mesh)
        # deal with silly mismatch between mesh dimensions and answer dimensions
        self.slope = sp.transpose(answer)[0]
        if (self.debug): print self.slope
    
    def calculateDisplacements(self):
        # initialize position arrays
        self.x = sp.zeros(self.numPoints)
        self.y = sp.zeros(self.numPoints)
        # take trig functions for position integrals
        xInt = sp.cos(self.slope)
        yInt = sp.sin(self.slope)
        # loop through and numerically integrate discrete functions
        mesh = sp.linspace(0, self.L, self.numPoints)
        for i,val in enumerate(mesh):
            self.x[i] = trapz(xInt[:i+1],mesh[:i+1])
            self.y[i] = trapz(yInt[:i+1],mesh[:i+1])
            
    def plotBeam(self,ax,legendLabel):
        ax.plot(self.x, self.y, label=legendLabel)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

    def showPlot(self):
        mpl.show()
        
    def printParameters(self):
        print '-'*50
        print 'beam modulus      =', self.E
        print 'beam thickness    =', self.t
        print 'beam width        =', self.w
        print 'moment of inertia =', self.I
        print 'beam length       =', self.L
        print 'grid points       =', self.numPoints
        print '-'*50

    def arcLengthIntegral(self, psiL):
        # this function returns the normalized arc length of
        # a beam using the arc length integral
        answer = quad(self.arcLengthElement,0,psiL,args=(psiL))[0]
        if (self.debug): 
            print 'normalized arc length = ',answer
            print 'psiL =', psiL
        return answer
        
    def arcLengthElement(self, psi, psiL):
        # this function is used to provide the integrand
        # for the normalized arc length        
        # how do i manage the singularity problem here during the solve routine?
        # if psiL is greater than pi/2, this will always return imaginary
        answer = 1/sqrt(sin(psiL)-sin(psi))
        # here my janky solution is to only take the absolute value
        answer = abs(answer)
        if (self.debug): 
            pass
            #print 'psi =',psi,'psiL =',psiL
            #print 'arcLengthElement =', answer
        return answer
    
    def beamLength(self,psiL,load):
        # takes normalized arclength and multiplies by dimensions
        # to scale to physical dimensions
        #return arcLengthIntegral(psiL)
        answer = self.arcLengthIntegral(psiL) * sqrt(self.E*self.I/2/self.shearLoad)
        if (self.debug): print 'physical arc length = ',answer
        return answer
    
    def solveFunction(self, psiL, load):
        # compares computed beam length as a function of end slope
        # to the measured beam length
        return self.L - self.beamLength(psiL,load)

    def derivative(self,psi, s):
        if (self.debug): print self.psiL
        factor = sp.sqrt(2*self.shearLoad/self.E/self.I)
        answer = sp.sqrt(sp.sin(self.psiL)-sp.sin(psi))
        return answer * factor

def main():
    E = 2e6           # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam

    thisBeam = beam()
    thisBeam.setBeamDimensions(L,t,w,E)
    load = 1e-5
    thisBeam.applyShearLoad(load)
    thisBeam.printParameters()
    thisBeam.calculateEndAngle()
    thisBeam.calculateSlopeFunction()
    thisBeam.calculateDisplacements()

    thatBeam = beam()
    thatBeam.setBeamDimensions(L,t,w,E)
    load = 1e-4
    thatBeam.applyShearLoad(load)
    thatBeam.printParameters()
    thatBeam.calculateEndAngle()
    thatBeam.calculateSlopeFunction()
    thatBeam.calculateDisplacements()

    
    figure = mpl.figure()
    ax = figure.add_subplot(111, aspect='equal')
    thisBeam.plotBeam(ax,'beam1')
    thatBeam.plotBeam(ax,'beam2')
    ax.legend()
    mpl.show()


    
if __name__ == '__main__':
    main()
