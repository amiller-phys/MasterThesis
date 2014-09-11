#!/usr/bin/env python2.7

"""
Program Doc String
"""

from __future__ import print_function, division
import sys, numpy, argparse
from math import sin,cos, pi
from scipy.integrate import odeint
from itertools import izip

#ATTEN - Give doc strings to individual dydt functs?
#ATTEN - Make scipy stream solutions?  Possible?

def main():
	"""
	Doc String
	"""

	options = parse_arguments()

	dydt = set_dydt(name = options.name, e = 0, mu = 0)

	solve_ODE(dydt = dydt, y0 = [pi/2-.1,0], method = 'rk4')


def parse_arguments():
	""" Parses arguments from the command line """

	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('--name', '-n', type=str, default='spring',
		help = '''Name of system to simulate.  Can choose from: 'spring',
		'pendulum', 'clock', 'coupled_clocks', and 'coupled_driven_clocks'.''')

	return parser.parse_args()

def set_dydt(name, mu = 7, e = 1.13, gamma = 0.12, l = 1.0, M = 5, k = 0.1, 
			c=1, m = 0.1, epsilon = 0, g = 9.8):
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
			return [x[1], -sin(x[0]) - mu*x[1] + e*cos(t)]

	if(name == 'clock'):
		def dydt(x, t):
			return [x[1], -sin(x[0]) - mu*x[1] + e*(gamma**2 - x[0]**2)*x[1]
					+ epsilon*cos(t)]

	#X[i] 0=theta1,1=theta1v,2=theta2,3=theta2v,4=x,5=v
	if(name == 'coupled_clocks'): 
		def D(t,theta, thetav):
			return e*(gamma**2 - theta**2)*thetav

	if(name == 'coupled_driven_clocks'):
		def D(t,theta, thetav):
			return epsilon*cos(t) - mu*thetav

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

def solve_ODE(dydt, y0, method = 'scipy'):
	"""
	"""

	if(method == 'scipy'):
		t  = numpy.linspace(0, 100., 5000)
		soln = odeint(dydt, y0, t)
		X = soln[:,0]
		Y = soln[:,1]
		if(name == 'coupled_clocks' or name == 'coupled_driven_clocks'):
			X2 = soln[:,2]
			Y2 = soln[:,3]
		soln = numpy.column_stack((t,soln))
		numpy.savetxt(sys.stdout,soln,delimiter=',', fmt='%.15f')

	elif(method == 'rk4'):
		position = y0
		t  = numpy.linspace(0, 100., 5000)
		dt = t[1]-t[0]

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