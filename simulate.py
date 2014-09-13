#!/usr/bin/env python2.7

"""
simulate.py use numerical methods to simulate a spring, pendulum, clock,
coupled clocks, and coupled driven clocks.  The positional argument specifies
the name of the system.  Initial conditions are set with --y0.  Additional
simulation parameters can be specified (all with reasonable defaults, see 
below).  Results are printed in csv format to stdou.  The first line of the
output is a header.
"""

from __future__ import print_function, division
import sys, numpy, argparse
from math import sin, cos, pi
from scipy.integrate import odeint
from itertools import izip

def main():
	"""
	Prases options from the command line, sets the derivative function dydt
	for the system secified in the command line, and then solves the ODE.
	First a header is printed, then results are printed to stdout in csv format.
	"""

	args = parse_arguments()

	dydt = set_dydt(name = args.name, mu = args.mu, e = args.e, l = args.l,
		gamma = args.gamma, M = args.M, k = args.k, c = args.c, m = args.m,
		epsilon = args.epsilon, g = args.g)

	print_header(name = args.name)

	solve_ODEs(dydt = dydt, time = args.time, dt = args.dt, y0 = args.y0, 
		method = args.method)


def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('name', type=str, default='spring',
		help = '''Name of system to simulate.  Can choose from: 'spring',
		'pendulum', 'clock', 'coupled_clocks', and 'coupled_driven_clocks'.
		Defaults to 'spring'.''')

	#Simulation Parameters
	parser.add_argument('--y0', '-y', type=float, nargs='+', default = [3,0],
		help = '''Sepcifies the list of initial conditions.  Defaults to
		[3,0], which only works with systems of 2 degrees of freedom (the 
		non coupled systems).  The coupled systems have 6 degrees of freedom,
		which requires a list of length 6 (i.e. [0,0,1.3,0,1.1,0]).''')
	parser.add_argument('-dt', type=float, default = 0.05,
		help = "Step size used in simulation (default 0.05).")
	parser.add_argument('--time', '-t', type=float, default=100,
		help = "Number of seconds simulated (default 100).")
	parser.add_argument('--method', type=str, default='scipy',
		help = '''Sepcify either 'rk4' to use a fourth-order Runge-Kutta
		method or 'scipy' to use odeint in scipy (default).''')
	
	#System Parameters
	parser.add_argument('-mu', type=float, default = 0,
		help='Damping parameter (defaults to 0)')
	parser.add_argument('-e', type=float, default = 1.13,
		help='Strength of escapment (defaults 1.13)')
	parser.add_argument('-gamma', type=float, default = 0.012,
		help='Critical angle of escapment (default 0.012)')
	parser.add_argument('-l', type=float, default = 1.0,
		help='Length of pendulum')
	parser.add_argument('-M', type=float, default = 5,
		help='Mass of common support')
	parser.add_argument('-k', type=float,default = 0.1,
		help='Spring constant (default 0.1)')
	parser.add_argument('-c', type=float, default=1,
		help='Damping parameter for common support')
	parser.add_argument('-m', type=float, default=0.1,
		help='Mass of pendulum point mass (default 0.1)')
	parser.add_argument('-epsilon', type=float, default=0,
		help='Strength of driving force (default 0)')
	parser.add_argument('-g', default=9.81,
		help='Acceleration of gravity (default 9.81)')

	args = parser.parse_args()

	if(len(args.y0) == 2 and (args.name == 'spring' 
		or args.name == 'pendulum' or args.name == 'clock')):
		return args
	elif(len(args.y0) == 6 and (args.name == 'coupled_clocks'
		or args.name == 'coupled_driven_clocks')):
		return args
	else:
		args.y0 = [0,0,1.3,0,1.1,0]
		return args

def set_dydt(name, mu = 7, e = 1.13, gamma = 0.12, l = 1.0, M = 5, k = 0.1, 
			c=1, m = 0.1, epsilon = 0, g = 9.81):
	"""
	Pre-condiiton: 'name' is the name of a system to simulate.  Parameters
	for the given system can be specified (given reasonable default values).

	Post-condition: returns a derivative function, dydt(x,t), for the given
	system.  'x' is a list giving the position in phase space, and dydt(x,t) 
	returns the derivative of x.
	"""

	if(name == 'spring'):
		def dydt(x, t):
			return [x[1], -x[0]-mu*x[1]]

	if(name == 'pendulum'):
		def dydt(x, t):
			return [x[1], -sin(x[0]) - mu*x[1] + epsilon*cos(t)]

	if(name == 'clock'):
		def dydt(x, t):
			return [x[1], -sin(x[0]) - mu*x[1] + e*(gamma**2 - x[0]**2)*x[1]
					+ epsilon*cos(t)]

	#Next two functions define escapments.
	if(name == 'coupled_clocks'): 
		def D(t,theta, thetav):
			return e*(gamma**2 - theta**2)*thetav

	if(name == 'coupled_driven_clocks'):
		def D(t,theta, thetav):
			return epsilon*cos(t) - mu*thetav

	#X[i] 0=theta1,1=theta1v,2=theta2,3=theta2v,4=beam,5=beamv
	if(name == 'coupled_clocks' or name == 'coupled_driven_clocks'):
		def xa(x,t):
			EscTerm = D(t,x[0],x[1])*cos(x[0])/l + D(t,x[2],x[3])*cos(x[2])/l

			Numerator1 = (m*g/2.0)*(sin(2*x[0]) + sin(2*x[2])) - k*x[4] - c*x[5]
			Numerator2 =  m*l*(x[1]**2*sin(x[0]) + x[3]**2*sin(x[2]))
			
			Denominator = M + m*(2.0 - cos(x[0])**2 - cos(x[2])**2)

			return (Numerator1 + Numerator2 - EscTerm)/Denominator

		def theta1a(x,t):

			Numerator = D(t,x[0],x[1]) - g*m*l*sin(x[0]) - m*l*xa(x,t)*cos(x[0])

			return Numerator/(m*l**2)

		def theta2a(x,t):

			Numerator = D(t,x[2],x[3]) - g*m*l*sin(x[2]) - m*l*xa(x,t)*cos(x[2])

			return Numerator/(m*l**2)

		def dydt(x,t):
			return [x[1],theta1a(x,t),x[3],theta2a(x,t),x[5],xa(x,t)]

	return dydt

def print_header(name):
	"""
	Pre-condition: name is either 'spring', 'pendulum', 'clock', 'coupled_clocks',
	or 'coupled_driven_clocks'.
	Post-condition: Prints approriate column headers to stdout.
	"""

	if(name == 'spring' or name == 'pendulum' or name == 'clock'): 
		print('time,position,velocity')
	elif(name == 'coupled_clocks' or name =='coupled_driven_clocks'): 
		print('time,theta1,theta1v,theta2,theta2v,beam,beam_v')

def solve_ODEs(dydt, y0, time = 100.0, dt = 0.05, method = 'scipy'):
	"""
	Pre-condiiton: dydt is a function, dydt(x,t), where x is a list of length n
	and t is time (n is the number of degrees of freedom).
	"""

	if(method == 'scipy'):
		t  = numpy.linspace(0, time, time/dt + 1)
		soln = numpy.column_stack((t,odeint(dydt, y0, t)))
		numpy.savetxt(sys.stdout,soln,delimiter=',', fmt='%.15f')

	elif(method == 'rk4'): #ATTEN - Double check time dependence
		position = y0
		t  = numpy.linspace(dt, time, time/dt)
		print(0,str(position).strip('[]'),sep=',')

		for i in t:
			k1 = dydt(position,i)
			k2 = dydt([y + 0.5*dt*k for y,k in izip(position, k1)],i)
			k3 = dydt([y + 0.5*dt*k for y,k in izip(position, k2)],i)
			k4 = dydt([y + dt*k for y,k in izip(position, k3)],i)

			position = [y + (dt/6)*(h1 + 2*h2 + 2*h3 + h4) for y,h1,h2,h3,h4 
				in izip(position,k1,k2,k3,k4)]

			print(i,str(position).strip('[]'),sep=',')

if __name__ == "__main__" :
    sys.exit(main())