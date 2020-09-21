#!/usr/bin/python
#
# A 1D gauss point function and derivative example.
# Written by Sven at 2017-04-03 for Garching ExaHyPE RSC presentation.
# May be used for different stuff, thought.
#
# This script is originally part of the Guidebook; the plots were used
# for a talk. Now it is part of the thesis.
#
# Author SvenK
#

from pylab import *
import sympy
from sympy import var, lambdify
#from aderdg.lagrangeInterpolation import * # aderdg package in engine/misc

# defining the single function we need from that package here:

def LagrangePoly(x,Lx, Ly):
    """
    Returns the Lagrange interpolation polynomial corresponding to the support points Lx 
    and nodal values Ly as symbolic expression.
    Algorithm was obtained from http://stackoverflow.com/questions/27744475/lagrange-interpolation-in-python-as-a-result-matematical-formula

    Parameters
    ----------
    x: symbolic variable
       Symbolic variable.
    Lx : list
       The support points.
    Ly : list
       Nodal values associated with the support points.
    Returns
    -------
    L: symbolic expression
       The Lagrange interpolation polynomial as symbolic expression.
    """
    if  len(Lx)!= len(Ly):
        print "ERROR"
        return 1
    symbolic_function=0
    for k in range ( len(Lx) ):
        t=1
        for j in range ( len(Lx) ):
            if j != k:
                t=t* ( (x-Lx[j]) /(Lx[k]-Lx[j]) )
        symbolic_function+= t*Ly[k]
    return symbolic_function



ion()

gausspoints=genfromtxt("gausspoints.txt", names=True)
outdir=lambda fname: fname #"output/"+fname

p = 5
mask = gausspoints['order'] == p
gwp = gausspoints[mask]['gaussLegendreNodes']

domain = linspace(0,1,100)

# style
lw = 2.5
ms = 15

def set_style(titlestr=""):

	use_latex_style = True
	LabelSize=20
	if use_latex_style:
		# Publication latex plot settings
		params = {
		'text.usetex'       : True,
		'xtick.major.size'  : 6,
		'xtick.minor.size'  : 3,
		'ytick.major.size'  : 6,
		'ytick.minor.size'  : 3,
		}
		mpl.rcParams.update(params) 
		plt.rc('font', family='serif', serif='Times')
	
		# LabelSize: requires to write
		#      ax.set_xlabel(r"$\mathcal{C}_{\rm 1.6} = M_{\rm TOV}/R_{1.6}$",size=LabelSize)
		#      ax.legend(shadow=False, frameon=False,fontsize=LabelSize-4,ncol=2)
		#      ax.tick_params(length=8, width=1.5, which='major',direction='in',color='black',labelsize=LabelSize)
		# Publication latex plot settings
		gca().tick_params(length=8, width=1.5, which='major',direction='in',color='black',labelsize=LabelSize)

	fig, ax = gcf(), gca()
	fig.patch.set_facecolor('white')
	matplotlib.rcParams.update({'font.size': LabelSize})

	# to avoid jumping of plots
	fig.set_size_inches( 8.15  ,  4.1875)
	ylim(-1.45, 1.6)
	xlim(0,1)

	if False:
		def adjust_spines(ax, spines):
		    for loc, spine in ax.spines.items():
			if loc in spines:
			    spine.set_position(('outward', 10))  # outward by 10 points
			    spine.set_smart_bounds(True)
		            spine.set_linewidth(lw)
			else:
			    spine.set_color('none')  # don't draw spine

		    # turn off ticks where there is no spine
		    if 'left' in spines:
			ax.yaxis.set_ticks_position('left')
		    else:
			# no yaxis ticks
			ax.yaxis.set_ticks([])

		    if 'bottom' in spines:
			ax.xaxis.set_ticks_position('bottom')
		    else:
			# no xaxis ticks
			ax.xaxis.set_ticks([])

		adjust_spines(ax, ['left', 'bottom'])
	ax.get_yaxis().set_ticks([]) # hide y ticks
	ax.get_xaxis().set_ticks([0,1])
	ylabel("Field", fontsize=LabelSize)#, rotation=0)
	xlabel("Single cell (patch)", fontsize=LabelSize)
	#if(titlestr): title(titlestr)
	fig.tight_layout() # actually brings texts back in

	# legendre grid lines
	[ax.axvline(x=xi, ls='--', color='lightgrey') for xi in gwp]

# test function
clf(); set_style("Interpolated initial data")
funccolor = "red"
#func = lambda x: sin(x**2 *8) /exp(x**2)*x**0.8
func = lambda x: sin(x*2*pi*2)
plot(domain, func(domain), color=funccolor, linewidth=lw)
plot(gwp, func(gwp), "o", color=funccolor, clip_on=False, markersize=ms)
savefig(outdir("01_initial.pdf"))

# projection onto DG polynomial
#clf();
set_style("Projection on DG polynomial")
projcolor = "forestgreen"
x = var("x")
projection = LagrangePoly(x, gwp, func(gwp))
numproj = lambdify(x, projection)
plot(domain, numproj(domain), color=projcolor, linewidth=lw)
plot(gwp, numproj(gwp), "o", color=projcolor, clip_on=False, markersize=ms)
savefig(outdir("02_projection.pdf"))

# derivative, faked
#clf();
set_style("DG derivative")
derivcolor = "blue"
deriv = sympy.diff(projection, x)
numderiv = lambdify(x, 0.04 * deriv)
plot(domain, numderiv(domain), color=derivcolor, linewidth=lw)
plot(gwp, numderiv(gwp), "o", color=derivcolor, clip_on=False, markersize=ms)
savefig(outdir("03_derivative.pdf"))

# A FD derivative:
clf()
set_style("FD derivative")
funccolor = "red"
eps = 0.02
stencil = lambda p: p + eps*array([-2, -1, 1, 2]) # stencil omitting zero
fd_offgrids = array(list(flatten(map(stencil, gwp))))
plot(domain, func(domain), color=funccolor, linewidth=lw)
plot(fd_offgrids, func(fd_offgrids), "o", color=derivcolor, clip_on=False, markersize=0.7*ms)
plot(gwp, func(gwp), "o", color=funccolor, clip_on=False, markersize=ms)
savefig(outdir("04_fd_local_derivs.pdf"))


# evaluation points
#plot(gwp, func(gwp), "D", color=funccolor, markersize=15.0)

# plot faked gradient
#gradcolor = "red"
#grad = 2*pi * gradient(func(domain))
#plot(domain, grad, color=gradcolor, linewidth=1.5)
#
#gwpgrad = interp(gwp, domain, grad)
#plot(gwp, gwpgrad, "o", color=gradcolor, markersize=15.)



