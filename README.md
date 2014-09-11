This is a list of the programs for my masters thesis, and what they intend to accomplish.

===================================================================

# Simulation:
Run numeric simulation, output numeric file to stdout

## Input
None (just argparse)

## ArgParse:

System parameters 
Damping (Mu), Drive Amp/Escapment Strength (Epsilon/e), gamma (critical angle)
-biff='Forcing' or 'Frequency' or 'Damping' (turns bifurcation on)
-biff_range = LIST (range of Forcings, Freqs, or Dampings to run)

-M, k, c, m, l, g

## Program Notes:

All that changes from system to system is diff eqs.

class dyn_system:
* Functions:
	* __init__
	* simulate(time)
	* derivs
* Data:
	* data
	* M,k,c,m,l,g; Mu,e,gamma


### Systems:
-Spring (SHM) (viewed as Phase Portrain, Time Series, )
	-Damped Spring (DON'T MAKE SEPARATE THAN NON-DAMPPED)
-Pendulum
-Clock (also limit cycle)
-Driven pendulum (also Poincare section)
-Driven pendulum Bifurcation Diagram (needs own since varing Forcing Amp, freq, damping )
-Coupled clocks (time series, sum/diff angle)
-Driven coupled clocks (phase portraits, limit cycle, biffurcation)

## Output:

Time series data in csv format.
* Header with Name of vars for plotting.  
* Should match if multiple (x,y) pairs (?)

===================================================================

# Transform Program:

## Input
CSV File (time series) from stdin
## Notes:

* Sum/diff angles
* Create Poincare Sections (subset data)
* Limit cycle
(Bifurcation needs to be part of simulation, nothing for here)

## Output
CSV file, to stdout, ready for plotting.

===================================================================

# Graphics Program:

## Program Notes:

* Handel plotting one or two (or multiple) systems (based on input)
* Make multiple plots based on one simulation run?  Might need to save \
simulation to txt file.


## Input:

* csv file with header (Used to label axis).  Plots points in pairs of two, read in as (x,y).
* need multiple header lines? (give name to each set of points,perhaps plot title)?
Probably not - only needed in the critical damping plot, that's unique enough to make a separate program.


## ArgParse:

* Specify xlim, ylim (options with defaults)
* Specify output image size (in pixels)
* Type of plot (time series, phase portrait)
* Type of graph (plot points, connected lines)

Input numeric simulation (possibly with some header), output graphics

Pipe program together for different resuls

Use a makefile to produce all needed graphics for thesis (and thesis).

# Critical Damping Program
* Seems like a special case to make classification plot & find critical damping.

-Error for exact systems (separate program)

===================================================================

# MultiSims Program:

## Program Notes:

* Creates multiple plots (i.e. Phase Portraits) on the same graph (useful for creating multiple pendulum, spring phase portraits).
* This was *not* used to create time-series for the two pendulums, as that was part of one simulation.


=====================================================================

# Bifurcatoin Program:

## Program Notes:

* Creates bifurcation diagram, varying one parameter.

===================================================================

# Error Analysis