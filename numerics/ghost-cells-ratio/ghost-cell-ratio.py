#!/usr/bin/env python2
# Small plot about ghost cell ratio for phd thesis numerics intro

from pylab import *
ion()


use_latex_style = True
if use_latex_style:
	# Publication latex plot settings
	params = {
	#'figure.figsize'    : [ 5.86,  7.45], # in inch # done at bottom
	'text.usetex'       : True,
	'xtick.major.size'  : 6,
	'xtick.minor.size'  : 3,
	'ytick.major.size'  : 6,
	'ytick.minor.size'  : 3,
	}
	mpl.rcParams.update(params) 
	plt.rc('font', family='serif', serif='Times')
	LabelSize=20
	# LabelSize: requires to write
	#      ax.set_xlabel(r"$\mathcal{C}_{\rm 1.6} = M_{\rm TOV}/R_{1.6}$",size=LabelSize)
	#      ax.legend(shadow=False, frameon=False,fontsize=LabelSize-4,ncol=2)
	#      ax.tick_params(length=8, width=1.5, which='major',direction='in',color='black',labelsize=LabelSize)
	# Publication latex plot settings

# Cubic cells, x is the extend
x = linspace(0,40)

volume = lambda dim: x**dim
ratio2d = lambda w: volume(2) / ( 4*x*w +   w**2)
ratio3d = lambda w: volume(3) / (12*x*w + 8*w**3 + 6*x**2*w)

ratio = ratio2d

# fill bad area
fill_between([0,100],[0,0],[1,1], color="gray", alpha=0.3)

# w is the ghost layer width (~ order of scheme / 2)
for w  in [1,2,3]:
	#p = plot(ratio2d(w), "--", alpha=0.5)
	plot(x, ratio3d(w), label=w)#, color=p[0].get_color())


ylim(0,2)
xlim(1,20)

from matplotlib.ticker import MaxNLocator
gca().xaxis.set_major_locator(MaxNLocator(integer=True))
locator_params(axis='x', nbins=5)
locator_params(axis='y', nbins=5)

xlabel("Patch size $x$")
ylabel("Ghost cell over physical cell ratio $R$")

l = legend(title="ghost layer\nwidth $w$", loc=2)
l.get_frame().set_alpha(0)

# read off current size with: gcf().get_size_inches()
gcf().set_size_inches(2.9, 3.93)
tight_layout()

def save():
	savefig("ghost-cell-ratio.pdf")
	savefig("ghost-cell-ratio.png")

save()
