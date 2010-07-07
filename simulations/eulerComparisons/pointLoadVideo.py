import matplotlib.pyplot as mpl
import numpy as np
import matplotlib.font_manager as font
from datetime import datetime
import os
import sys
sys.path.append('../')
import taperedElasticaBeam as teb

def initFigure():
    height = 6.5
    width = 6.5
    fig = mpl.figure()
    fig.set_figwidth(width)
    fig.set_figheight(height)
    ax = fig.add_axes((0.1,0.4,0.8,0.55))
    ax.set_xlim(0,60)
    ax.set_ylim(0,60)
    ax.set_autoscalex_on(False)
    ax.set_autoscaley_on(False)
    ax.set_aspect('equal')
    ax.grid()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    figDictionary = {'fig': fig, 'ax': ax}
    return figDictionary

def initColors():
    return ['b','g','r','c','m','y','k']

def elastica(beam, pointLoad, fig, legend, color):
    beam.setShearLoad(pointLoad)
    beam.calculateSlopeFunction()
    beam.calculateDisplacements()
    scale = 1e6
    fig['ax'].plot(scale*beam.x, scale*beam.y, color=color)
    loadString = str(int(pointLoad*scale)) + ' $\mu$N - elastica'
    legend.append(loadString)


def euler(beam, pointLoad, fig, legend, color):
    scale = 1e6
    x = np.linspace(0, beam.L, beam.numPoints)
    displacement = ((-pointLoad/(6*beam.E*beam.I))
                        * (x**3 - 3*beam.L*x**2))
    fig['ax'].plot(x*scale, displacement*scale, color)
    loadString = str(int(pointLoad*scale)) + ' $\mu$N - euler'
    legend.append(loadString)

def addChartJunk(beam, figure, pointLoad, elasticaLegends, eulerLegends):
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
    mpl.title('elastica vs euler point load models')

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
    figure['ax'].legend(labels, ncol = 2, bbox_to_anchor = (1.1, -.1))

def saveFile(fig, imageNumber, dateCode):
    plotFileName = ('pointLoadVideo/pointLoadDivergence ' + dateCode
    				+ '-' + str(imageNumber) + '.png')
    fig.savefig(plotFileName, transparent=True)


def main():
    numPointLoads = 100
    pointLoad = np.linspace(.1e-6,18e-6,numPointLoads)

    L = 60e-6
    Lt = 120e-1
    t = 20e-6
    w = 20e-6
    E = 1e6

    beam = teb.taperedElasticaBeam()
    beam.setBeamDimensions(L=L, Lt=Lt, t=t, w=w, E=E)

    dateCode = datetime.now().strftime('%Y%m%d%H%M')

    for i, j in zip(pointLoad, range(numPointLoads)):
        elasticaLegends = []
        eulerLegends = []
        fig = initFigure()
        elastica(beam=beam, pointLoad=i, fig=fig, legend=elasticaLegends, color='b')
        euler(beam=beam, pointLoad=i, fig=fig, legend=eulerLegends, color='r')
        addChartJunk(beam=beam, figure=fig, pointLoad=i,
                 elasticaLegends=elasticaLegends, eulerLegends=eulerLegends)
        saveFile(fig=fig['fig'], imageNumber=j, dateCode=dateCode)
        mpl.close()


if __name__ == '__main__':
    main()