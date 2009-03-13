#!/usr/bin/env python
# taperedBeam.m
# plot of spring constant of a tapered beam in lateral bending
# see lab book 2008_1 pg. 94
# 

import enthought.traits.api              as ta
import enthought.traits.ui.api           as tua
import enthought.chaco.api               as ca 
import enthought.enable.component_editor as ece
import numpy                             as np

# define constants

class taperedBeam(ta.HasTraits):
    a = ta.Array
    k = ta.Array
    base = ta.Range(low=10,high=30,value=20)
    length = ta.Range(low = 50,high=80,value = 60)
    modulus = ta.Range(low = 100, high = 200, value =175)
    myPlot = ta.Instance(ca.Plot)
    
    def __init__(self):
        super(taperedBeam,self).__init__()
        self.a = np.arange(0.0,1.00,0.05)
        self.createPlot()
        
    def calcK(self):
        b = self.base*10**-6
        l = self.length*10**-6
        m = self.modulus*10**4
        self.k = ((self.a - 1)**3 * b**4 * m /
                  (6 * (2 * np.log(self.a) + self.a**2 - 4 * self.a + 3) * 
                   l**3))
    
    def createPlot(self):
        self.calcK()
        self.plotdata = ca.ArrayPlotData(a=self.a,k=self.k)
        self.myPlot = ca.Plot(self.plotdata)
        self.myPlot.plot(('a','k'),type='line', color='blue')
        titleString = ('base = ' + str(self.base) + '\n' +
                       'length = ' + str(self.length) + '\n' + 
                       'modulus = ' + str(self.modulus))
        self.myPlot.title = titleString
        self.myPlot.value_range.set_bounds(0,0.1)

    @ta.on_trait_change('base,length,modulus')
    def replot(self):
        self.createPlot()

    traits_view = tua.View(tua.Item('myPlot',
                             editor = ece.ComponentEditor(),
                             show_label = False),
                       tua.Item(name = 'base'),
                       tua.Item(name = 'length'),
                       tua.Item(name = 'modulus'))
                       

myTaperedBeam = taperedBeam()
myTaperedBeam.configure_traits()
