#!/usr/bin/env python
'''
create a visual representation of dalquist criterion
by simulating a fractalish surface and the deformation
of an adhesive material to that surface
'''

import numpy             as np
import numpy.random      as nr
import matplotlib.pyplot as mpl

# seed random number generator

# number of frequency components
N = 200
# scaling exponent
p = 0.9

# create vector of random phases
nr.seed(1)
phase = nr.rand(N)

x = np.linspace(0,2*3.14,5000)
#y = np.sin(x + phase[0])
y = np.zeros(len(x))
for i in range(N):
    if i//2 == 1:
        y = y + 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i])
    else:
        y = y - 1/(i+1)**p*np.sin((i+1)*x + 2*3.14*phase[i])

y = y + 4

# turn off axes and grid
#mpl.plot(x,y)
mpl.fill_between(x,y,y2=0)
mpl.show()

'''
y = 0;
x = 0:.001:2*3.14;
rand('state',0);
phase = 2*3.14*rand([1,N]);

for i = 1:N
	y = y + 1/i^(.7)*sin(i*x + phase(i));
	if i==round(N/2) y2=y+2; end
	if i==round(N/4) y4=y+4; end
	if i==round(N/8) y8=y+6; end
	
end

y9=zeros(1,length(x))+9;

hold off
plot (x,y,'k')
axis([0,2*3.14,-10,12])
hold on
plot (x,y2,'k')
plot (x,y4,'k')
plot (x,y8,'k')
plot (x,y9,'k')

'''