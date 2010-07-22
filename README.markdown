Tapered Beam Analysis Code
==========================
This code is meant to provide an elastica solution for the
calculation of the profile of tapered and non-tapered beams.

Example Use
-----------
    # instantiate
    beam = teb.taperedElasticaBeam()

    # set dimensions and modulus
    beam.setBeamDimensions(L,Lt,t,w,E)

    # desired end angle of beam
    endAngle = sp.pi / 2
    beam.setEndAngle(endAngle)

    # shear bending load
    shearLoad = 1e-6
    beam.setShearLoad(shearLoad)

    # axial load
    axialLoad = 1e-6
    beam.setAxialLoad(axialLoad)

    # solve psi(s) function
    beam.calculateSlopeFunction()

    # convert psi(s) to cartesian
    beam.calculateDisplacements()

    # plot beam position
    beam.plotBeam(ax,'legend title')

Test Code
---------
The tests directory contains testCode.py.  This is a script
that will perform a few tests of the taperedElasticaBeam.py
(teb) library.

Simulation Code
-------------
The simulations directory contains various calculations and
simulations using the teb library.
