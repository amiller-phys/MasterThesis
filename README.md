This is a list of the programs for my masters thesis, and what they intend to accomplish.

# Systems/Plots:
-Spring (SHM) (viewed as Phase Portrain, Time Series)
	-Damped Spring (DON'T MAKE SEPARATE THAN NON-DAMPPED)
-Pendulum
-Clock (also limit cycle)
-Driven pendulum (also Poincare section)
-Driven pendulum Bifurcation Diagram (needs own since varing Forcing Amp, freq, damping )
-Coupled clocks (time series, sum/diff angle)
-Driven coupled clocks (phase portraits, limit cycle, biffurcation)

===================================================================

# Simulation:
Run numeric simulation, output numeric file to stdout (in csv format) 

## Notes:

* Add check if scipy is installed (make so can run just on built in rk4 method).
To check it, just add /usr/bin/ to front of python2.7 in shebang line.

* Double check DiffEQs to make sure correct.

* Investigate other ODE methods (i.e. non-uniform time-step).

===================================================================

# Transform Program:

## Input
CSV File (time series) from stdin.  Does the following transformations:
* Sum/diff of given vars
* Poincare Sections (subset data)
* Limit cycle

## Output
CSV file, to stdout, ready for plotting.

## Notes:
* PS and LC just subset the data (horizontal slices).
* Sum/Diff require more work, to manage the approriate columns.

For poincare, must make sure that t % args.time == 0 (pick step size and time well, otherwise you'll get nothing (or little by chance)).  Check cut off.  ATTEN - Let user specifiy threshold cutt off????

===================================================================

# Graphics Program:

## Notes:

* Figure out how to connect the dots
* Possible to do multiple phase portrate plots?

===================================================================

# MultiSims Program:

## Program Notes:

* Creates multiple plots (i.e. Phase Portraits) on the same graph (useful for creating multiple pendulum, spring phase portraits).
* This was *not* used to create time-series for the coupled clocks, as that was part of one simulation.


=====================================================================

# Bifurcatoin Program:

## Program Notes:

Creates bifurcation diagram, varying one parameter.

## ArgParse:
* -biff='Forcing' or 'Frequency' or 'Damping' (turns bifurcation on)
* -biff_range = LIST (range of Forcings, Freqs, or Dampings to run)

===================================================================

# Error Analysis (for exact systems)

===================================================================

# Critical Damping

===================================================================

# Makefile
