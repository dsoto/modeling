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


class elasticaBeam:
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    #I = t**3 * w / 12.0  # moment of inertia for rectangular beam
    L = 60e-6            # length of beam (m)
    numPoints = 100      # number of grid points for ODE
    debug = False
    shearLoad = 1e-6     # transverse load on beam (N)
    psiL = 0             # angle at end of beam (radians)
    xL = 0
    yL = 0

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

    def setDebug(self, debug):
        self.debug = debug

    def applyShearLoad(self, shearLoad):
        self.shearLoad = shearLoad

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

    def plotBeam(self,ax,legendLabel):
        scale = 1e6
        ax.plot(scale*self.x, scale*self.y, label=legendLabel)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

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

    def printParameters(self):
        print '-' * 50
        print 'beam modulus                =', self.E
        print 'beam thickness              =', self.t
        print 'beam width                  =', self.w
        print 'moment of inertia           =', self.I
        print 'beam length                 =', self.L
        print 'grid points                 =', self.numPoints
        print 'applied shear load          =', self.shearLoad
        print 'y (shear) tip displacement  =', self.yL
        print 'x tip displacement          =', self.xL
        print 'lateral spring constant     =', self.springConstant
        print '-' * 50

    def printResults(self):
        print '-' * 50
        print 'x displacement    =', self.xL
        print 'y displacement    =', self.yL
        print 'final angle       =', self.psiL

    def calculateSlopeFunction(self):
        if (self.debug):
            print 'entered calculateSlopeFunction'
        # here we call the solve function
        # initial condition = bending moment / modulus / moment of inertia
        guess = self.shearLoad * self.L / self.E / self.I / 3
        #guess = 30000
        if (self.debug):
            print 'initial derivative guess =', guess
        initialDerivative = fsolve(self.solveFunction, guess)
        if (self.debug):
            print 'initialDerivative =', initialDerivative

    def solveFunction(self, initialDerivative):
        if (self.debug):
            print 'entering solveFunction'
        mesh = sp.linspace(0, self.L, self.numPoints)
        initialCondition = zeros(2)
        initialCondition[0] = 0
        initialCondition[1] = initialDerivative
        # this answer will be the slope function and its first derivative
        answer = odeint(self.derivative, initialCondition, mesh)
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
        d = zeros(2)
        d[0] = Psi[1]
        # derivative function for normal beam
        d[1] = -self.shearLoad / self.E / self.I * cos(Psi[0])
        return d

    def calculateSpringConstant(self, load):
        self.applyShearLoad(load)
        self.calculateSlopeFunction()
        self.calculateDisplacements()
        self.springConstant = self.shearLoad / self.yDisplacement()
        return self.springConstant

def main():
    E = 2e6           # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam

    thisBeam = elasticaBeam()
    thisBeam.setBeamDimensions(L,t,w,E)
    load = 1e-5
    thisBeam.applyShearLoad(load)
    thisBeam.printParameters()
    thisBeam.calculateSlopeFunction()
    thisBeam.calculateDisplacements()

    thatBeam = elasticaBeam()
    thatBeam.setBeamDimensions(L,t,w,E)
    load = 5e-5
    thatBeam.setDebug(True)
    thatBeam.applyShearLoad(load)
    thatBeam.printParameters()
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
