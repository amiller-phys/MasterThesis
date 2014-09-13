#!/usr/bin/env python2.7

"""
transform.py performs can compute the sum or difference of two columns, a 
limit cycle (taking only data where t > --time), or a Poincare section (taking 
data every --time seconds) of csv data read from stdin.  The first line read must
be a header giving the columns names.  The positional argument specifies the
type of transformation to preform.  The optional argument -x and -y can be used
to specify the name of the columns to be used for the sum (commputing x + y) 
and difference (computing x - y).
"""

from __future__ import print_function, division
import sys, argparse

def main():
	"""
	Parses arguments from the command line, reads the header from stdin, then
	determines the approriate indicies to be used in the transformations, prints
	the proper header for the transformed data.  The reaming csv data is read
	from stdin.  It is then transformed then printed to stdout.
	"""

	args = parse_arguments()

	#header is a list of the column names.
	#first_index is the index of the first column used in the sum/diff.
	#second_index is the index of the second column used in the sum/diff.

	header = sys.stdin.readline().strip().split(',')	
	if(args.trans == 'sum' or args.trans == 'diff'):
		print('time',args.trans,sep=',')
	else: print(','.join(header))

	if(args.first is not None and args.second is not None):
		first_index = header.index(args.first)
		second_index = header.index(args.second)
	else:
		first_index, second_index = 1,3

	for line in sys.stdin:
		x = [float(i) for i in line.strip().split(',')]
		if(args.trans == 'sum'): 
			y = x[first_index] + x[second_index]
			print(x[0],y,sep=',')
		elif(args.trans == 'diff'): 
			y = x[first_index] - x[second_index]
			print(x[0],y,sep=',')
		elif(args.trans == 'limit_cycle' and x[0] >= args.time):
			print(line.strip())
		elif(args.trans == 'poincare' and x[0] % args.time < 1e-15):
			print(line.strip())
			

def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('trans', type=str,
		help='''Specifies the type of transformation to perform. Choices 
		include 'sum', 'diff', 'poincare', and 'limit_cycle'.''')


	parser.add_argument('--time', '-t', type=float, default=30,
		help = '''For limit cycles, all data after this time is printed.
		For poincare sections, this time represent the sample frequence
		(data is printed every t seconds).  Defaults to 30''')
	parser.add_argument('--first', '-f', '-x', type=str, default=None,
		help='''Name of the first column used in the sum/diff transformation.
		For the coupled systems, it defaults to theta1.''')
	parser.add_argument('--second', '-s', '-y', type=str, default=None,
		help='''Name of the second column used in the sum/diff transformation.
		For teh coupled systems, it defaults to theta2.''')

	return parser.parse_args()

if __name__ == "__main__" :
    sys.exit(main())