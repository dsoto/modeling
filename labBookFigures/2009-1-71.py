#!/usr/bin/env python


from __future__ import print_function
import sys
sys.path.append('..')
import taperedElasticaBeam as teb
import scipy               as sp
import matplotlib          as mpl
import matplotlib.pyplot   as plt

E = 2e6           # modulus of pdms
t = 19e-6           # thickness of beam
w = 19e-6           # width of beam
L = 52e-6           # length of beam


def plotBeam(Lt,suffix):

    thisBeam = teb.taperedElasticaBeam()
    lengthInContact = sp.linspace(0,20,11) * 1e-6
    endAngle = sp.pi / 2

    figure = plt.figure()
    # figure size and resolution
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    ax.set_aspect('equal')

    for i, thisLength in enumerate(lengthInContact):
        thisBeam.setBeamDimensions(L - thisLength, Lt, t, w, E)
        thisBeam.calculateSlopeFunctionForEndAngle(endAngle)
        thisBeam.addSlopeWithLength(endAngle, thisLength)
        thisBeam.calculateDisplacements()
        thisBeam.plotBeam(ax,str(thisLength))

    ax.grid()
    ax.legend(loc='best')

    from datetime import datetime
    import os
    string  = ('length = '+str(L*1e6)+' microns'+'\n'+
               'thickness = '+str(t*1e6)+' microns'+'\n'+
               'width = '+str(w*1e6)+' microns'+'\n'+
               'modulus = '+str(E/1e6)+' MPa'+'\n'+
               'taper length = '+str(Lt*1e6)+' microns' +'\n'+
               datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
               os.path.abspath(__file__))

    xPos = 0.5
    yPos = 0.05
    plt.figtext(xPos, yPos, string,
                ha='center')

    # name plot same as script
    fileName = os.path.basename(__file__)
    fileName = os.path.splitext(fileName)[0]
    plotFileName = fileName + '-' + suffix + '.pdf'
    figure.savefig(plotFileName, transparent=True)

def main():

    Lt = 1000000e-6         # length of taper
    plotBeam(Lt, '1')

    Lt = 60e-6
    plotBeam(Lt, '2')


if __name__ == "__main__":
    main()