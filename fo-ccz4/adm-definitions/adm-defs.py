#!/usr/bin/env python2
from pylab import *
ion()

X = linspace(-1,1)

x0 = array([ -.5, 0, .5 ])

#T = array([ 0, 0.25, 0.4, 0.7 ])
# T: Function of space x
T = array([
	lambda x: 0 * ones_like(x),
	lambda x: 0.25 * ones_like(x),
	lambda x: 0.4 * ones_like(x),
	lambda x: 0.7 * ones_like(x) ])

x = ndarray((len(T),len(x0)))

x[0] = x0
x[1] = x0+.25
x[2] = [ -1, 0, 1 ]
x[3] = x0**3 - .25

for i,_ in enumerate(x):
	plot(x[i], T[i](x0), "o",
		color="red")
	plot([-1,1], T[i](x0), "-",
		color="black")

for i,_ in enumerate(x[:-1]):
	quiver(
		x[i],T[i](x0),
		(x[i+1]-x[i])*ones_like(X),
		T[i+1](x0)-T[i](x0),
		angles="xy", scale=1, scale_units="xy",
		color="blue")

#xlim(0,1)
#ylim(0,1)

