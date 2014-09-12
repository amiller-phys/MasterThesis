#!/usr/bin/env python2.7

"""
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import sys, argparse
from itertools import izip
from matplotlib.backends.backend_pdf import PdfPages

def main():
	"""
	Parses arguments, plots point (expand).
	"""

	args = parse_arguments()

	#Read in header, decided how to precide based on header length!
	header = sys.stdin.readline().strip().split(',')
	x_indices = [header.index(i) for i in args.x]
	y_indices = [header.index(i) for i in args.y]

	for line in sys.stdin:
		point = line.split(',')
		for x_index, y_index, color in izip(x_indices, y_indices, args.colors):
			plt.plot(point[x_index],point[y_index], color)

	if(args.xmax is not None): plt.xlim(xmax = args.xmax)
	if(args.xmin is not None): plt.xlim(xmin = args.xmin)
	if(args.ymax is not None): plt.ylim(ymax = args.ymax)
	if(args.ymin is not None): plt.ylim(ymin = args.ymin)

	if(args.xlab is not None): plt.xlabel(args.xlab)
	if(args.ylab is not None): plt.ylabel(args.ylab)
	if(args.title is not None): plt.title(args.title)
	
	if(args.output is None): plt.show()
	else: plt.savefig(args.output, format='pdf')

def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('-x', type=str, nargs='+', default=['Position'])
	parser.add_argument('-y', type=str, nargs='+', default=['Velocity'])
	parser.add_argument('--colors', '-c', type=str, nargs='+', default=['b.'])

	#Axis limit parameters
	parser.add_argument('--xmax', type=float, default=None)
	parser.add_argument('--xmin', type=float, default=None)
	parser.add_argument('--ymax', type=float, default=None)
	parser.add_argument('--ymin', type=float, default=None)

	#ATTEN - add option to do axis limits all at once. Mutually exclusive group?
	#ATTEN - Add option to connect the dots (if possible)
	#ATTEN - Image size parameters

	#Labels - x-axis, y-axis, and plot title
	parser.add_argument('--xlab', type=str, default=None)
	parser.add_argument('--ylab', type=str, default=None)
	parser.add_argument('--title', type=str, default=None)
	#http://stackoverflow.com/questions/12444716/how-do-i-set-figure-title-and-axes-labels-font-size-in-matplotlib

	#Output results
	parser.add_argument('--output','-o', type=str, default=None)

	return parser.parse_args()

if __name__ == "__main__":
	sys.exit(main())