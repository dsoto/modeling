#!/usr/bin/env python

import enthought.traits.api              as ta
import enthought.traits.ui.api           as tua
import enthought.chaco.api               as ca 
import enthought.enable.component_editor as ece
import numpy                             as np

# define constants

class taperedBeam(ta.HasTraits):
    x = ta.Array(comparison_mode = 0)
    y = ta.Array(comparison_mode = 0)
    load = ta.Range(low=10,high = 30,value = 20)
    moment = ta.Range(low=10,high=30,value=20)
    length = ta.Range(low = 50,high=80,value = 60)
    loadPoint = ta.Range(low = 0, high = 80, value = 50)
    modulus = ta.Range(low = 100, high = 200, value =175)
    myPlot = ta.Instance(ca.Plot)
    plotdata = ta.Instance(ca.ArrayPlotData)
    
    def __init__(self):
        super(taperedBeam,self).__init__()
        self.createPlot()
        
    def calcY(self):
        # split x index up based on
        self.x = np.arange(0.0,self.length,1)
        # print 'length x = ',len(self.x)
        index = self.loadPoint/1
        ## print self.x[index]
        x1 = self.x[0:index]
        # print 'length x1 = ',len(x1)
        x2 = self.x[index:]
        # print 'length x2 = ',len(x2)
        # had to cast as float to hack around weird roundoff bug
        y1 = (self.load * x1**2 / 6 / float(self.modulus) / 
              self.moment * (3 * self.loadPoint - x1)) 
        # print 'length y1 = ',len(y1)
        # print 'load point = ',self.loadPoint
        # print 'x value at transition',x2[0]
        y2 = (self.load * self.loadPoint**2 / 6/ float(self.modulus)/
              self.moment * (3 * x2 - self.loadPoint))
        # print 'length y2 = ',len(y2)
        # print 'y1 at boundary = ',y1[-1]
        # print 'y2 at boundary = ',y2[0]
        self.y = np.concatenate((y1,y2))
        self.y = self.y
        self.x = self.x
        # print self.x
        # print self.y

    def createPlot(self):
        self.calcY()
        self.plotdata = ca.ArrayPlotData(x=self.x,y=self.y)
        self.myPlot = ca.Plot(self.plotdata)
        self.myPlot.plot(('x','y'),type='line', color='blue')
        titleString = ('load = ' + str(self.load) + '\n' +
                       'length = ' + str(self.length) + '\n' + 
                       'modulus = ' + str(self.modulus))
        self.myPlot.title = titleString

    @ta.on_trait_change('load,moment,length,loadPoint,modulus')
    def replot(self):
        self.calcY()
        self.plotdata.set_data('y',self.y)
        self.plotdata.set_data('x',self.x)
        self.createPlot()


    traits_view = tua.View(tua.Item('myPlot',
                             editor = ece.ComponentEditor(),
                             show_label = False),
                       tua.Item(name = 'load'),
                       tua.Item(name = 'length'),
                       tua.Item(name = 'moment'),
                       tua.Item(name = 'loadPoint'),
                       tua.Item(name = 'modulus'))
                       

myTaperedBeam = taperedBeam()
myTaperedBeam.configure_traits()
