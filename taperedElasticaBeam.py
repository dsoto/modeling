#!/usr/bin/env python

# Noe is testing changing stuff

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
    lengthInContact = 20e-6


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

    '''
    methods for calculation of beam profile with point moment.
    
    this is achieved by setting the angle that we want
    the end of the beam to be and then applying the proper
    moment to achieve that angle.
     '''

    def calculateSlopeFunctionForEndAngle(self, angle):
        pass
        # this function applies a moment at the end of the
        # beam to get the end angle to be the specified angle
        bendingMoment = 0
        solution = fsolve(self.solveFunctionForEndAngle,
                          bendingMoment,
                          args = (angle,))
        return solution

    def solveFunctionForEndAngle(self, bendingMoment, angle):
        self.mesh = sp.linspace(0, self.L, self.numPoints)
        initialCondition = 0
        answer = odeint(self.derivativeForEndAngle,
                        initialCondition,
                        self.mesh,
                        args = (bendingMoment,))

        self.slope = answer[:,0]
        # return last element of slope function
        return angle - self.slope[-1]

    def derivativeForEndAngle(self, psi, s, bendingMoment):
        # this needs to be able to use different values for
        # the bending moment applied
        return bendingMoment / self.E / self.moment(s)



    '''
    methods for the calculation of beam profile with point load
    applied at end of beam
    '''
    def calculateSlopeFunctionForPointLoad(self):
        self.calculateSlopeFunction()

    def calculateSlopeFunction(self):
        # this function uses fsolve to find the initial derivative
        # of the slope function that will make the derivative at
        # the end of the beam zero
        #
        # initial condition = bending moment / modulus / moment of inertia
        guess = self.shearLoad * self.L / self.E / self.I
        #guess = 90000
        initialDerivative = fsolve(self.solveFunction, guess)
        if (self.debug):
            print 'initialDerivative =', initialDerivative

    def solveFunction(self, initialDerivative):
        # this function takes an initial derivative of the
        # slope function, integrates the ODE and returns
        # the derivative at the slope function at the end
        # of the beam
        # this function is called by calculateSlopeFunction
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


    '''
    methods for properties of beam used in solve functions.
    beam thickness, derivatives for ODE, moment of area
    '''
    def derivative(self, Psi, s):
        # returns the derivatives for the beam function
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

# method to create flat length in contact for
# plotting purposes

    def addSlopeWithLength(self, slope, length):
        # add a length of slopes to simulate the beam in side contact
        self.lengthInContact = length
        slopeArray = slope * sp.ones(int(self.numPoints/self.L*length))
        self.slope = sp.hstack([self.slope, slopeArray])

# methods for reporting beam profile and information

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
        # use length of slope array
        self.x = sp.zeros(len(self.slope))
        self.y = sp.zeros(len(self.slope))

        # take trig functions for position integrals
        xInt = sp.cos(self.slope)
        yInt = sp.sin(self.slope)
        # loop through and numerically integrate discrete functions
        mesh = sp.linspace(0, self.L+self.lengthInContact, len(self.slope))
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

    def xTipDisplacement(self):
        return self.xL

    def yTipDisplacement(self):
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

    def calculateSpringConstant(self, load):
        beam.applyShearLoad(load)
        beam.calculateSlopeFunction()
        beam.calculateDisplacements()
        beam.springConstant = load / beam.yTipDisplacement()

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
    Lt = 100e-6         # length of taper

    thisBeam = taperedElasticaBeam()
    thisBeam.setBeamDimensions(L,Lt,t,w,E)
    #load = 1e-5
    #thisBeam.applyShearLoad(load)
    thisBeam.printParameters()
    #thisBeam.calculateSlopeFunctionForPointLoad()
    #thisBeam.calculateDisplacements()
    endAngle = sp.pi / 2
    thisBeam.debug = True
    thisBeam.calculateSlopeFunctionForEndAngle(endAngle)
    print thisBeam.slope
    thisBeam.calculateDisplacements()
    figure = mpl.figure()
    ax = figure.add_subplot(111, aspect='equal')
    thisBeam.plotBeam(ax,'thisBeam')
    ax.legend(loc='best')
    mpl.show()

if __name__ == '__main__':
    main()
