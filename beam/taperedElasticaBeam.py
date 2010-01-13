#!/usr/bin/env python
'''
December 30, 2009 5:25:17 PM -0800
i have taken elasticaBeam.py and renamed it to
taperedElasticaBeam.pyplot

i plan to implement a profile solution for a tapered
beam using the elastica formulation

i need to code a system of coupled differential 
equations to solve the second-order equation
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
'''

class taperedElasticaBeam:
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    I = t**3 * w / 12.0  # moment of inertia for rectangular beam
    L = 60e-6            # length of beam (m)
    Lt = 120e-1          # length of taper (m) at Lt beam has zero thickness
    numPoints = 100      # number of grid points for ODE
    debug = False
    shearLoad = 1e-6     # transverse load on beam (N)
    psiL = 0             # angle at end of beam (radians)
    xL = 0
    yL = 0
    slopeCalculated = False
    

    def __init__(self):
        pass
        
    def setBeamDimensions(self, L, Lt, t, w, E):
        self.L  = L
        self.Lt = Lt
        self.t  = t
        self.w  = w
        self.E  = E
        self.I  = t**3 * w / 12.0
        
    def setNumPoints(self, numPoints):
        self.numPoints = numPoints
        
    def applyShearLoad(self, shearLoad):
        self.shearLoad = shearLoad
                
    def calculateSlopeFunction(self):
        pass
        # here we call the solve function
        # initial condition = bending moment / modulus / moment of inertia
        guess = self.shearLoad * self.L / self.E / self.I
        guess = 90000
        initialDerivative = fsolve(self.solveFunction, guess)
        print 'initialDerivative =', initialDerivative

    def solveFunction(self, initialDerivative):
        if (self.debug):
            print 'entering solveFunction'
        self.mesh = sp.linspace(0, self.L, self.numPoints)
        initialCondition = zeros(2)
        initialCondition[0] = 0
        initialCondition[1] = initialDerivative
        # this answer will be the slope function and its first derivative
        answer = odeint(self.derivative, initialCondition, self.mesh)
        # we store the slope function (the first column) as a member variable
        self.slope = answer[:,0]
        # we take the last element of the second column
        # this is the change in slope at the end of the beam
        # which should be zero
        self.slopeDerivative = answer[:,1]
        if (self.debug): 
            #print self.slope
            print 'starting slope derivative =', self.slopeDerivative[0]
            print 'ending slope derivative =', self.slopeDerivative[self.numPoints-1]
        return self.slopeDerivative[self.numPoints-1]
 
    def derivative(self, Psi, s):
        if (self.debug):
            print 'entering derivative'
        d = zeros(2)
        d[0] = Psi[1]
        # derivative function for normal beam
        #d[1] = -self.shearLoad / self.E / self.I * cos(Psi[0])
        # derivative function for tapered beam
        d[1] = ( -self.shearLoad / self.E * cos(Psi[0])
                 -self.momentDerivative(s) * Psi[1]) / self.moment(s)
        if (self.debug):
            print 'first derivative  =', d[0]
            print 'second derivative =', d[1]
        return d

    def moment(self, s):
        thisMoment = 1.0 / 12.0 * self.w * self.thickness(s)**3
        if (self.debug):
            print 'width =', self.w * 1e6
            print 'thickness =', self.thickness(s) * 1e6
            print 'arc length =', s * 1e6
        if (self.debug):
            print 'moment =', thisMoment
        #return self.t**3 * self.w / 12.0
        return thisMoment
    
    def momentDerivative(self, s):
        thisMD = 1.0 / 4.0 * self.w * self.thickness(s)**2 * (-self.t) / self.Lt
        if (self.debug):
            print 'arclength =', s
            print 'moment derivative =', thisMD
        #return 0
        return thisMD
        
    def thickness(self, s):
        thisThickness = self.t * (1 - s / self.Lt)
        return thisThickness
        
    def printParameters(self):
        print '-' * 50
        print 'beam modulus      =', self.E
        print 'beam thickness    =', self.t * 1e6
        print 'beam width        =', self.w * 1e6
        print 'moment of inertia =', self.I
        print 'beam length       =', self.L * 1e6
        print 'taper length      =', self.Lt * 1e6
        print 'grid points       =', self.numPoints
        print '-' * 50

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
        self.xL = self.x[self.numPoints-1]
        self.yL = self.y[self.numPoints-1]
            
    def plotBeam(self, ax, legendLabel):
        scale = 1e6
        ax.plot(scale*self.x, scale*self.y, label=legendLabel)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

    def plotSlope(self, ax, legendLabel):
        scale = 1e6
        ax.plot(scale*self.mesh, self.slope, label=legendLabel)
        ax.set_xlabel('Arc Length ($\mu$m)')
        ax.set_ylabel('Beam Slope (rad)')
        
    def plotCurvature(self, ax, legendLabel):
        scale = 1e6
        ax.plot(scale*self.mesh, self.slopeDerivative, label=legendLabel)
        ax.set_xlabel('Arc Length ($\mu$m)')
        ax.set_ylabel('Beam Curvature (m$^{-1}$)')

    def plotRadiusOfCurvature(self, ax, legendLabel):
        scale = 1e6
        ax.plot(scale*self.mesh, 
                1/abs(self.slopeDerivative)*scale, label=legendLabel)
        ax.set_ylim((0,100))
        ax.set_xlabel('Arc Length ($\mu$m)')
        ax.set_ylabel('Radius of Curvature ($\mu$m)')

    def showPlot(self):
        mpl.show()
    
    def xDisplacement(self):
        return self.xL
        
    def yDisplacement(self):
        return self.yL
    
    def stringParameters(self):
        returnString = r'beam modulus      = ' + str(self.E) + '\n'
        returnString +=  'beam thickness    ='+ str(self.t) + '\n'
        returnString +=  'beam width        ='+ str(self.w) + '\n'
        returnString +=  'beam length       ='+ str(self.L) + '\n'
        return returnString

    def setDebug(self, debug):
        self.debug = debug
        
    def printResults(self):
        print '-' * 50
        print 'x displacement    =', self.xL
        print 'y displacement    =', self.yL
        print 'final angle       =', self.psiL
        
        
'''
algorithm for finding beam profile

- guess starting value of dpsi/ds
- calculate beam based on starting guess
- check if beam has dpsi/ds = 0 at end of beam
- if dpsi/ds != 0, vary starting guess
    - can i use fsolve here by passing back the end slope?
    
we can check the validity of these results by using a very shallow
taper and comparing to the untapered elastica beam

'''

def main():
    E = 2e6           # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam
    Lt = 100e1         # length of taper

    thisBeam = taperedElasticaBeam()
    thisBeam.setBeamDimensions(L,Lt,t,w,E)
    load = 1e-5
    thisBeam.applyShearLoad(load)
    thisBeam.printParameters()
    thisBeam.calculateSlopeFunction()
    thisBeam.calculateDisplacements()
    
    figure = mpl.figure()
    ax = figure.add_subplot(111, aspect='equal')
    thisBeam.plotBeam(ax,'thisBeam')
    ax.legend()
    mpl.show()



if __name__ == '__main__':
    main()
