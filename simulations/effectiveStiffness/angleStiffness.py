import matplotlib.pyplot as mpl
import numpy as np
import sys
sys.path.append('../../')
import taperedElasticaBeam as teb

##################################################################
# creates a beam and sets its properties (angle not included)
def initBeam():
    E = 1e6              # elastic modulus of beam (Pa)
    t = 20e-6            # dimension of beam in bending direction (m)
    w = 20e-6            # width of beam (m)
    L = 60e-6            # length of beam (m)
    Lt = 120e-6          # length of taper (m) at Lt beam has zero thickness

    beam=teb.taperedElasticaBeam()
    beam.setBeamDimensions(E=E, t=t, w=w, L=L, Lt=Lt)

    return beam

##################################################################
# creates the figure and axes, returns a tuple (fig, ax)
def initFig():
	figHeight = 6
	figWidth = 6
	fig = mpl.figure()
	fig.set_figheight(figHeight)
	fig.set_figwidth(figWidth)

	ax = fig.add_axes([.2,.2, .8,.5])
	ax.grid()
	ax.set_xlabel('Angle')
	ax.set_ylabel('Effective Stiffness')

	return (fig, ax)

##################################################################
# takes the specified test load normal to the surface of the
# cantelever and translates it to a shear and normal load with
# respect to the beam.
def setLoads(beam, angle, force):
	normal = force*np.cos(angle)
	shear = force*np.sin(angle)
	beam.setAxialLoad(axialLoad=normal)
	beam.setShearLoad(shearLoad=shear)

##################################################################
# calculates displacement at the tip of the beam, then uses that
# to find the change in length normal to the cantelever (dx).
# using the known force normal to the cantelever, k is calculated
# as though the beam were a linear spring.
def calculateStiffness(beam, angle, force):
	beam.calculateSlopeFunction()
	beam.calculateDisplacements()
	xTipInitial = beam.L
	xTipFinal = beam.xTipDisplacement()
	dx = (xTipInitial - xTipFinal)*np.cos(angle)
	k = force/dx
	return k

##################################################################
# takes the stiffness (k from previous method) and plots it on the
# axes.
def plotPoint(stiffness, fig, ax, angle):
	ax.plot(angle, stiffness, 'ro')

##################################################################
# annotates the plot, saves it as a pdf
#def chartJunk(fig=fig):

##################################################################
# finds the effective stiffness of a tapered beam that is tilted
# at an angle with respect to the surface of a force cantelever.
# the effective stiffness is found for the direction normal to
# the surface of the cantelever by measuring the change in length
# in that direction. the specified test load is divided by this
# change in length to get the effective spring constant k.
def main():

	force = 1e-6							#test load in micronewtons
	beam=initBeam()
	fig=initFig()

	angleDeg = np.linspace(-45,45,90)			#0 is perp to cantelever
	angleRad = angleDeg*np.pi/180

	for (i,v) in zip(angleDeg, angleRad):					#i=deg, v=rad
		setLoads(beam=beam, angle=v, force=force)							#in rad
		stiffness = calculateStiffness(beam=beam, angle=v, force=force)		#in rad
		plotPoint(stiffness=stiffness, fig=fig[0], ax=fig[1], angle=i)		#in deg
#	chartJunk(fig)

main()