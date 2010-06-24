Tapered Beam Analysis Code
==========================

This code is meant to provide an elastica solution for the
calculation of the profile of tapered and non-tapered beams.

Example Use
-----------

    beam.setBeamDimensions(L,Lt,t,w,E)
    endAngle = sp.pi / 2
    beam.setEndAngle(endAngle)
    shearLoad = 10e-6
    beam.setShearLoad(shearLoad)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'both loads')
