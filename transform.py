#!/usr/bin/env python2.7

"""
transform.py performs various transformations on csv data read from stdin.
First line is read as a header (unless --no_header specified)
"""

from __future__ import print_function, division
import sys, argparse

def main():
	"""
	"""

	args = parse_arguments()

	if(args.header): header = sys.stdin.readline().strip().split(',')

	if(len(header) == 3): #systems w/ 2 degrees of freedom + time

		#ATTEN - RIGHT NOW ONLY SET UP FOR LC/PS
		print(','.join(header))
		for line in sys.stdin:
			t,x,y = line.strip().split(',')
			t = float(t) #ATTEN - better way?

			if(args.trans == 'limit_cycle' and t >= args.time):
				print(t,x,y,sep=',')
			elif(args.trans == 'poincare' and t % args.time < 1e-15):
				print(t,x,y,sep=',')

	if(len(header) == 7): #systems w/ 6 degrees of freedom + time
		first_index = header.index(args.first)
		second_index = header.index(args.second)

		#ATTEN - RIGHT NOW ONLY SET UP FOR SUM/DIFF
		print('Time',args.trans,sep=',')
		for line in sys.stdin:
			x = [float(i) for i in line.strip().split(',')] #ATTEN - better way?
			if(args.trans == 'sum'): y = x[first_index] + x[second_index]
			elif(args.trans == 'diff'): y = x[first_index] - x[second_index]
			print(x[0],y,sep=',')
			

def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('trans', type=str, default='limit_cycle',
		help='''Specifies the type of transformation to perform. Choices 
		include 'sum', 'diff', 'poincare', and 'limit_cycle'.''')
	parser.add_argument('--no_header', dest='header', action='store_false',
		help = '''Prints header if this is specified (default False)''')

	parser.add_argument('--time', '-t', type=float, default=30,
		help = '''For limit cycles, all data after this time is printed.
		For poincare sections, this time represent the sample frequence
		(data is printed every t seconds).  Defaults to 30''')

	parser.add_argument('--first', '-f', type=str, default='Theta1')
	parser.add_argument('--second', '-s', type=str, default='Theta2')

	return parser.parse_args()

if __name__ == "__main__" :
    sys.exit(main())