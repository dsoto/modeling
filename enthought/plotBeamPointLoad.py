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
    load = ta.Range(low=10,high = 100,value = 20)
    moment = ta.Range(low=10,high=30,value=20)
    length = ta.Range(low = 50,high=80,value = 60)
    width = ta.Range(low = 10, high = 30, value = 20)
    loadPoint = ta.Range(low = 0, high = 80, value = 50)
    modulus = ta.Range(low = 100, high = 200, value =175)
    myPlot = ta.Instance(ca.Plot)
    plotdata = ta.Instance(ca.ArrayPlotData)
    
    def __init__(self):
        super(taperedBeam,self).__init__()
        self.createPlot()
        
    def calcY(self):
        l = self.length * 10**-6
        p = self.load * 10**-6
        I = self.moment * 10**-24
        w = self.width * 10**-6
        I = w**4 / 12
        a = self.loadPoint * 10**-6
        m = self.modulus * 10**5
        nPts = 100
        self.x = np.linspace(0.0, l, nPts)
        index = a / l * nPts
        x1 = self.x[0:index]
        x2 = self.x[index:]
        y1 = (p * x1**2 / 6 / float(m) / I * (3 *  a - x1)) 
        y2 = (p *  a**2 / 6 / float(m) / I * (3 * x2 - a ))
        self.y = np.concatenate((y1,y2))
        self.y = self.y * 10**6
        self.x = self.x * 10**6

    def createPlot(self):
        self.calcY()
        self.plotdata = ca.ArrayPlotData(x=self.x,y=self.y)
        self.myPlot = ca.Plot(self.plotdata)
        self.myPlot.plot(('x','y'),type='line', color='blue')
        self.myPlot.value_range.set_bounds(0,100)
        titleString = ('load = ' + str(self.load) + '\n' +
                       'length = ' + str(self.length) + '\n' + 
                       'modulus = ' + str(self.modulus))
        self.myPlot.title = titleString

    @ta.on_trait_change('load,width,moment,length,loadPoint,modulus')
    def replot(self):
        self.calcY()
        self.plotdata.set_data('y',self.y)
        self.plotdata.set_data('x',self.x)
        self.createPlot()


    traits_view = tua.View(tua.Item('myPlot',
                             editor = ece.ComponentEditor(),
                             show_label = False),
                       tua.Item(name = 'load'),
                       tua.Item(name = 'width'),
                       tua.Item(name = 'length'),
                       tua.Item(name = 'moment'),
                       tua.Item(name = 'loadPoint'),
                       tua.Item(name = 'modulus'))
                       

myTaperedBeam = taperedBeam()
myTaperedBeam.configure_traits()
