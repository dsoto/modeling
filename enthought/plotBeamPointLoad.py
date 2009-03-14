#!/usr/bin/env python

import enthought.traits.api              as ta
import enthought.traits.ui.api           as tua
import enthought.chaco.api               as ca 
import enthought.enable.component_editor as ece
import numpy                             as np

# define constants

class taperedBeam(ta.HasTraits):
    a = ta.Array
    k = ta.Array
    load = ta.Range(low=10,high = 30,value = 20)
    moment = ta.Range(low=10,high=30,value=20)
    length = ta.Range(low = 50,high=80,value = 60)
    loadPoint = ta.Range(low = 0, high = 80, value = 60)
    modulus = ta.Range(low = 100, high = 200, value =175)
    myPlot = ta.Instance(ca.Plot)
    
    def __init__(self):
        super(taperedBeam,self).__init__()
        self.x = np.arange(0.0,self.length,0.1)
        self.createPlot()
        
    def calcY(self):
          self.y = (self.load * self.x**2 / 6 / self.modulus / 
                    self.moment * (3*self.length-self.x)) 

    def createPlot(self):
        self.calcY()
        self.plotdata = ca.ArrayPlotData(x=self.x,y=self.y)
        self.plotdata.set_data('y',self.y)
        self.myPlot = ca.Plot(self.plotdata)
        self.myPlot.plot(('x','y'),type='line', color='blue')
        titleString = ('load = ' + str(self.load) + '\n' +
                       'length = ' + str(self.length) + '\n' + 
                       'modulus = ' + str(self.modulus))
        self.myPlot.title = titleString

    @ta.on_trait_change('load,moment,length,loadPoint,modulus')
    def replot(self):
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
