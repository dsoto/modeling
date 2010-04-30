import elasticaBeam as eb

E = 1.75e6             # modulus of pdms
t = 12.8e-6           # thickness of beam at base
w = 20.5e-6           # width of beam at base
I = t**3 * w / 12.0 # moment of inertia
L = 66.1e-6           # length of beam
load = 0.5e-6

beam = eb.elasticaBeam()

beam.setBeamDimensions(L,t,w,E)

beam.calculateSpringConstant(load)
beam.printParameters()

import matplotlib.pyplot as plt

figure = plt.figure()
axes = figure.add_axes((0.1,0.1,0.8,0.8),aspect = 'equal')
beam.plotBeam(axes,'legend')