#!/usr/bin/env python

from __future__ import print_function
import sys
sys.path.append('../')
import taperedElasticaBeam as teb
import scipy               as sp
import matplotlib          as mpl
import matplotlib.pyplot   as plt

def beamLoop(E,t,w,L,Lt,ax,label):

    beam = teb.taperedElasticaBeam()

    lengthInContact = sp.linspace(0,10,11) * 1e-6
    frictionFactor = 1
    shearForce = lengthInContact * frictionFactor
    shearForce = sp.zeros(len(lengthInContact))
    endAngle = sp.pi / 2
    curvature     = sp.zeros(len(lengthInContact))

    print(label)
    for i, thisLength in enumerate(lengthInContact):
        beam.setBeamDimensions(L - thisLength, Lt, t, w, E)
        beam.setEndAngle(endAngle)
        beam.setShearLoad(shearForce[i])
        beam.calculateSlopeFunction()
        beam.calculateDisplacements()
        curvature[i] = beam.slopeDerivative[-1]
        print('length    =', thisLength*1e6,   'um')
        #print('curvature =', curvature[i], '1/m')
        print('radius    =', 1/curvature[i]*1e6, 'um')
        tipThick = beam.thickness(L-thisLength)
        print('tip thick =', tipThick*1e6, 'um')
        print()

    ax.plot(lengthInContact*1e6,1/curvature*1e6,label = label)


def main():
    E = 2e6           # modulus of pdms
    t = 20e-6           # thickness of beam
    w = 20e-6           # width of beam
    L = 60e-6           # length of beam

    figure = plt.figure()
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    ax.set_xlabel('length in contact (microns)')
    ax.set_ylabel('radius of curvature (microns)')
    ax.grid()

    lTaper = [55e-6, 60e-6, 100e-6, 200e-6, 1, -100e-6]
    lTaper = [100e-6, 1]
    t = [10e-6, 10e-6]
    for i, Lt in enumerate(lTaper):
        label = 'Lt = %f m  t = %f m ' % (Lt,t[i])
        beamLoop(E,t[i],w,L,Lt,ax,label)

# plot as included angle on wedge

    ax.legend(loc='best')
    from datetime import datetime
    import os
    string  = ('length = '+str(L*1e6)+' microns'+'\n'+
               'width = '+str(w*1e6)+' microns'+'\n'+
               'modulus = '+str(E/1e6)+' MPa'+'\n'+
               datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
               os.path.abspath(__file__))

    xPos = 0.5
    yPos = 0.05
    plt.figtext(xPos, yPos, string,
                ha='center')

    # name plot same as script
    fileName = os.path.basename(__file__)
    fileName = os.path.splitext(fileName)[0]
    plotFileName = fileName + '.pdf'
    figure.savefig(plotFileName)


if __name__ == "__main__":
    main()