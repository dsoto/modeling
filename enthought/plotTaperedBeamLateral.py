#!/usr/bin/env python
# taperedBeam.m
# plot of spring constant of a tapered beam in lateral bending
# see lab book 2008_1 pg. 94
# 

from enthought.traits.api import HasTraits, Instance, Array, Range, Button, on_trait_change
from enthought.traits.ui.api import View, Item, Handler 
from enthought.chaco.api import Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
from enthought.traits.ui.menu import OKButton
from numpy import arange,log

# define constants

class taperedBeam(HasTraits):
    a = Array
    k = Array
    base = Range(low=10,high=30,value=20)
    length = Range(low = 50,high=80,value = 60)
    modulus = Range(low = 100, high = 200, value =175)
    myPlot = Instance(Plot)
    
    def __init__(self):
        super(taperedBeam,self).__init__()
        self.a = arange(0.0,1.00,0.05)
        self.createPlot()
        
    def calcK(self):
        b = self.base*10**-6
        l = self.length*10**-6
        m = self.modulus*10**4
        self.k = ((self.a - 1)**3 * b**4 * m /
                  (6 * (2 * log(self.a) + self.a**2 - 4 * self.a + 3) * 
                   l**3))
    
    def createPlot(self):
        self.calcK()
        self.plotdata = ArrayPlotData(a=self.a,k=self.k)
        self.myPlot = Plot(self.plotdata)
        self.myPlot.plot(('a','k'),type='line', color='blue')
        titleString = ('base = ' + str(self.base) + '\n' +
                       'length = ' + str(self.length) + '\n' + 
                       'modulus = ' + str(self.modulus))
        self.myPlot.title = titleString
        self.myPlot.value_range.set_bounds(0,0.1)

    @on_trait_change('base,length,modulus')
    def replot(self):
        self.createPlot()

    traits_view = View(Item('myPlot',
                             editor = ComponentEditor(),
                             show_label = False),
                       Item(name = 'base'),
                       Item(name = 'length'),
                       Item(name = 'modulus'))
                       

myTaperedBeam = taperedBeam()
myTaperedBeam.configure_traits()

#	k=(a - 1).^3*b^4*E./(6*(2*log(a) + a.^2 - 4.*a + 3)*L(i)^3);
#	# matlab can't deal with limit a->1 so we manually put in data point
#	k(length(k)+1)=b^4*E/L(i)^3/4;
#	a(length(a)+1)=1.0;
