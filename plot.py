#!/usr/bin/env python2.7

"""
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import sys, argparse

def main():
	"""
	"""

	plt.show()

	args = parse_arguments()

	#Read in header, decided how to precide based on header length!
	header = sys.stdin.readline().strip().split(',')
	x_index = header.index(args.x)
	y_index = header.index(args.y)

	for line in sys.stdin:
		point = line.split(',')
		plt.plot(point[x_index],point[y_index],'b.')

	plt.show()

def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('-x', type=str,default='Position')
	parser.add_argument('-y', type=str,default='Velocity')

	return parser.parse_args()

if __name__ == "__main__":
	sys.exit(main())