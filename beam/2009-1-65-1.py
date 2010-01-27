#!/usr/bin/env python

from __future__ import print_function
import taperedElasticaBeam as teb
import scipy               as sp
import matplotlib          as mpl
import matplotlib.pyplot   as plt

def main():
    E = 2e6           # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    L = 52e-6           # length of beam
    Lt = 60e-6         # length of taper
    #Lt = 1000000e-6         # length of taper
    
    thisBeam = teb.taperedElasticaBeam()
    lengthInContact = sp.linspace(0,10,11) * 1e-6
    endAngle = sp.pi / 2

    figure = plt.figure()
    # figure size and resolution
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    
    bendingMoment = sp.zeros(len(lengthInContact))
    curvature     = sp.zeros(len(lengthInContact))
    
    for i, thisLength in enumerate(lengthInContact):
        thisBeam.setBeamDimensions(L - thisLength, Lt, t, w, E)
        bendingMoment[i] = thisBeam.calculateSlopeFunctionForEndAngle(endAngle)
        thisBeam.calculateDisplacements()
        print(bendingMoment[i],end='\t')
        curvature[i] = thisBeam.derivativeForEndAngle(0, L - thisLength,
                                                      bendingMoment[i])
        print(curvature[i])
        #thisBeam.plotBeam(ax,str(thisLength))

    ax.plot(lengthInContact*1e6,1/curvature*1e6)
    ax.set_xlabel('length in contact (microns)')
    ax.set_ylabel('radius of curvature (microns)')
    ax.grid()

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
    plotFileName = fileName + '.pdf'
    figure.savefig(plotFileName, transparent=True)

    
if __name__ == "__main__":
    main()