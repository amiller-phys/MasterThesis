#!/usr/bin/env python2.7

"""
plot.py plots csv data (read from stdin) created by either simulation.py or 
transform.py.  Use '-y' to specify one (or more) volumn names to plot versus
'-x', which is used to specify one (or more) column names.  The number of names
given for -x must match the number of names given for -y.  Use -c option to
specify the color(s) to use in the plot.  Output is sent to the terminal, or
a pdf file if a name is specified with the -o option.
"""

from __future__ import print_function
import sys, argparse
import matplotlib.pyplot as plt
from itertools import izip_longest

def main():
	"""
	Parses arguments from the command line, reads the header from stdin, then
	deptermines the approritate indicies to be plotted.  As each data point is 
	read from stdin, the point is plotted.  The axes limits are adjusted, labels 
	added (if specified in the command line), then the plot is outputed (either
	to the terminal or to a pdf file if specified with -o option).
	"""

	args = parse_arguments()

	#header is a list of the column names.
	#x_indicies is a list of indicies to be plotted horizontoally (x-direction)
	#y_indicides is a list of indicies to be plotted vertically (y-direction)

	header = sys.stdin.readline().strip().split(',')
	x_indices = [header.index(i) for i in args.x]
	y_indices = [header.index(i) for i in args.y]

	for line in sys.stdin:
		point = line.split(',')
		for x_index, y_index, color in izip_longest(
					x_indices, y_indices, args.colors, fillvalue='b.'):
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

	parser.add_argument('-x', type=str, nargs='+', default=['position'])
	parser.add_argument('-y', type=str, nargs='+', default=['velocity'])
	parser.add_argument('--colors', '-c', type=str, nargs='+', default=['b.'])

	#Axis limit parameters
	parser.add_argument('--xmax', type=float, default=None)
	parser.add_argument('--xmin', type=float, default=None)
	parser.add_argument('--ymax', type=float, default=None)
	parser.add_argument('--ymin', type=float, default=None)

	#Labels - x-axis, y-axis, and plot title
	parser.add_argument('--xlab', type=str, default=None)
	parser.add_argument('--ylab', type=str, default=None)
	parser.add_argument('--title', type=str, default=None)
	#http://stackoverflow.com/questions/12444716/how-do-i-set-figure-title-and-axes-labels-font-size-in-matplotlib

	#Output results
	parser.add_argument('--output','-o', type=str, default=None)

	args = parser.parse_args()

	if len(args.x) != len(args.y):
		raise Exception('''Lenght of arguments for -x MUST equal the length of 
			arguments given to -y''')

	if len(args.colors) > len(args.x):
		args.colors = args.colors[0:len(args.x)]

	return args

if __name__ == "__main__":
	sys.exit(main())