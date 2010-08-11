import matplotlib.pyplot as mpl
import numpy as np
import matplotlib.font_manager as font
from datetime import datetime
import os
import sys
sys.path.append('../../')
import taperedElasticaBeam as teb

def initFigure():
    height = 6.5
    width = 6.5
    fig = mpl.figure()
    fig.set_figwidth(width)
    fig.set_figheight(height)
    ax = fig.add_axes((0.1,0.4,0.8,0.55))
    ax.set_aspect('equal')
    ax.grid()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    figDictionary = {'fig': fig, 'ax': ax}
    return figDictionary

def initColors():
    return ['b','g','r','c','m','y','k']

def elastica(beam, endAngle, fig, legend, color):
    beam.setEndAngle(endAngle)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    scale = 1e6
    fig['ax'].plot(scale*beam.x, scale*beam.y, color=color)
    degString = str(int(round(endAngle*180/np.pi)))
    legend.append(degString +' degrees - elastica')

def euler(beam, endAngle, fig, legend, color):
    scale = 1e6
    x = np.linspace(0, beam.L, beam.numPoints)
    M = endAngle*beam.E*beam.I / beam.L
    displacement = M*x**2 / (2*beam.E*beam.I)
    fig['ax'].plot(x*scale, displacement*scale, color)
    degString = str(int(round(endAngle*180/np.pi)))
    legend.append(degString +' degrees - euler')

def addChartJunk(beam, figure, endAngle, elasticaLegends, eulerLegends):
    plotFont = font.FontProperties()
    plotFont.set_size('small')
    dateString = datetime.now().strftime('%d %b %Y - %H:%M')
    string  = ('length = '+str(beam.L*1e6)+' microns'+'\n'+
               'thickness = '+str(beam.t*1e6)+' microns'+'\n'+
               'width = '+str(beam.w*1e6)+' microns'+'\n'+
               'modulus = '+str(beam.E/1e6)+' MPa'+'\n'+
               dateString+'\n' + os.path.abspath(__file__))
    xPos = 0.5
    yPos = 0.05
    mpl.figtext(xPos, yPos, string, ha='center')
    mpl.title('elastica vs euler end angle models')

    # sets location of legend outside the axes using bbox_to_anchor arg.
    # the cordinates seem to be based off of the axes; if you make the bottom
    # equal to 0 i.e. (.8, 0), the top of the legend Bbox will be right on
    # the x axis. i can't figure out how to get the legend centered, but .8
    # seems about right for the 6.5 by 6.5 figures.
    labels = []
    numPairs = range(len(elasticaLegends))
    for i in numPairs:
        labels.append(elasticaLegends[i])
        labels.append(eulerLegends[i])
    figure['ax'].legend(labels, ncol = 2, bbox_to_anchor = (1, -.1))

def saveFile(fig):
    dateCode = datetime.now().strftime('%Y%m%d%H%M')
    plotFileName = ('endAngleDivergence ' + dateCode + '.pdf')
    fig.savefig(plotFileName, transparent=True)

def main():
    toRadians = np.pi/180
    endAngleDeg = np.array([40, 50, 60], dtype=int)

    L = 60e-6
    Lt = 120e-1
    t = 20e-6
    w = 20e-6
    E = 1e6

    beam = teb.taperedElasticaBeam()
    beam.setBeamDimensions(L=L, Lt=Lt, t=t, w=w, E=E)

    fig = initFigure()
    colors = initColors()
    elasticaLegends = []
    eulerLegends = []

    for (offset, value) in enumerate(endAngleDeg):
        elastica(beam=beam, endAngle=value*toRadians, fig=fig,
                 legend=elasticaLegends, color=colors[offset])
        euler(beam=beam, endAngle=value*toRadians, fig=fig,
                 legend=eulerLegends, color=colors[offset])

    addChartJunk(beam=beam, figure=fig, endAngle=endAngleDeg,
                 elasticaLegends=elasticaLegends, eulerLegends=eulerLegends)

    saveFile(fig=fig['fig'])

if __name__ == '__main__':
    main()