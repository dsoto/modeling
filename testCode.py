import taperedElasticaBeam as tEB
import scipy as sp
import matplotlib.pyplot as mpl
from datetime import datetime
import os


def endAngleTest():
    ##########################################################
    # beam constants

    E = 2e6             # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam


    ##########################################################
    # defining figure

    figure = mpl.figure()
    # figure size and resolution
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    ax.set_aspect('equal')


    ##########################################################
    # tapered beam

    Lt = 100e-6         # length of taper

    thisBeam = tEB.taperedElasticaBeam()
    thisBeam.setBeamDimensions(L,Lt,t,w,E)
    endAngle = sp.pi / 2
    thisBeam.setEndAngle(endAngle)
    thisBeam.calculateSlopeFunction()
    thisBeam.calculateDisplacements()
    thisBeam.plotBeam(ax,'thisBeam')


    ##########################################################
    # non-tapered beam

    Lt = 1			#length of taper

    secondBeam = tEB.taperedElasticaBeam()
    secondBeam.setBeamDimensions(L,Lt,t,w,E)
    endAngle = sp.pi / 2
    secondBeam.setEndAngle(endAngle)
    secondBeam.calculateSlopeFunction()
    secondBeam.calculateDisplacements()
    secondBeam.plotBeam(ax,'nonTaperedBeam')



    ##########################################################
    # text below plot

    string  = ('length = '+str(L*1e6)+' microns'+'\n'+
               'thickness = '+str(t*1e6)+' microns'+'\n'+
               'width = '+str(w*1e6)+' microns'+'\n'+
               'modulus = '+str(E/1e6)+' MPa'+'\n'+
               'taper length = '+str(Lt*1e6)+' microns' +'\n'+
               datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
               os.path.abspath(__file__))
    xPos = 0.5
    yPos = 0.05
    mpl.figtext(xPos, yPos, string,
                ha='center')

    ax.legend()
    plotFileName = 'endAnglePlot-' + dateString + '.pdf'
    figure.savefig(plotFileName, transparent=True)

def pointLoadTest():
    ##########################################################
    # beam constants

    E = 2e6             # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam


    ##########################################################
    # defining figure

    figure = mpl.figure()
    # figure size and resolution
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    ax.set_aspect('equal')


    # instantiate beam
    beam = tEB.taperedElasticaBeam()

    ##########################################################
    # tapered beam

    Lt = 100e-6         # length of taper

    beam.setBeamDimensions(L,Lt,t,w,E)
    shearLoad = 10e-6
    beam.setShearLoad(shearLoad)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'beam')


    ##########################################################
    # non-tapered beam

    Lt = 1			#length of taper

    beam = tEB.taperedElasticaBeam()
    beam.setBeamDimensions(L,Lt,t,w,E)
    shearLoad = 10e-6
    beam.setShearLoad(shearLoad)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'nonTaperedBeam')



    ##########################################################
    # text below plot

    string  = ('length = '+str(L*1e6)+' microns'+'\n'+
               'thickness = '+str(t*1e6)+' microns'+'\n'+
               'width = '+str(w*1e6)+' microns'+'\n'+
               'modulus = '+str(E/1e6)+' MPa'+'\n'+
               'taper length = '+str(Lt*1e6)+' microns' +'\n'+
               datetime.now().strftime('%d %b %Y - %H:%M')+'\n'+
               os.path.abspath(__file__))
    xPos = 0.5
    yPos = 0.05
    mpl.figtext(xPos, yPos, string,
                ha='center')

    ax.legend()
    plotFileName = 'pointLoad-' + dateString + '.pdf'
    figure.savefig(plotFileName, transparent=True)

def allThreeTest():
    ##########################################################
    # beam constants

    E = 2e6             # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam

    dateString = datetime.now().strftime('%Y%m%d-%H%M%S')

    ##########################################################
    # defining figure

    figure = mpl.figure()
    # figure size and resolution
    width = 9
    height = 9
    figure.set_figheight(height)
    figure.set_figwidth(width)
    ax = figure.add_axes((0.1,0.4,0.8,0.55))
    ax.set_aspect('equal')


    beam = tEB.taperedElasticaBeam()


    #########################################################
    Lt = 100e-6         # length of taper

    beam.setBeamDimensions(L,Lt,t,w,E)
    endAngle = sp.pi / 2
    beam.setEndAngle(endAngle)
    shearLoad = 10e-6
    beam.setShearLoad(shearLoad)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'both loads')

    endAngle = sp.pi / 2
    beam.setEndAngle(endAngle)
    beam.setShearLoad(0)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'angle only')

    shearLoad = 10e-6
    beam.setShearLoad(shearLoad)
    beam.setEndAngle(0)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    beam.plotBeam(ax,'shear load only')

    ax.legend(loc='best')
    figureName = 'allThree-' + dateString + '.pdf'
    figure.savefig(figureName)


def main():
    # begin main program

    E = 2e6             # modulus of pdms
    t = 19e-6           # thickness of beam
    w = 19e-6           # width of beam
    I = t**3 * w / 12.0 # moment of inertia
    L = 52e-6           # length of beam

    dateString = datetime.now().strftime('%Y%m%d-%H%M%S')

    endAngleTest()
    pointLoadTest()
    allThreeTest()

if __name__ == '__main__':
    main()