# Simulation:
Run numeric simulation, output numeric file to stdout

## Input
None

## ArgParse:

System parameters (i.e damping, driving force)
* SHM = None (could add accell scaling)
* Damped_SHM = Mu
* Pendulum = None (could add scaling)
* Damped_Pend = Mu (v scalar)
* Driven_pend = Epsilon (*cos(t) in diffeq)
* Damped_Driven_pend = Mu
* Clock = Mu, e (escapement strencgth), gamma (critical angle)
* Driven Clock += Epsilon 

* -biff='Forcing' or 'Frequency' or 'Damping' (turns bifurcation on)
* -biff_range = LIST (range of Forcings, Freqs, or Dampings to run)

## Program Notes:

### Systems:
-Spring (SHM) (viewed as Phase Portrain, Time Series, )
-Damped Spring
-Pendulum
-Clock (also limit cycle)
-Driven pendulum (also Poincare section)
-Driven pendulum Bifurcation Diagram (needs own since varing Forcing Amp, freq, damping )
-Error for exact systems
-Coupled clocks (time series, sum/diff angle)
-Driven coupled clocks (phase portraits, limit cycle)

## Output:



# Transform Program:
* Add angles
* Create Poincare Sections (subset data)
* Limit cycle
(Bifurcation needs to be part of simulation, nothing for here)


===================



# Graphics Program:

## Program Notes:

* Handel plotting one or two (or multiple) systems (based on input)
* Make multiple plots based on one simulation run?  Might need to save \
simulation to txt file.
* Have option to manipulate data.  Separate program?


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