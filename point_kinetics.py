#!/usr/bin/python
"""Example use of the PointKineticsSolver"""

from PointKineticsSolver import PointKineticsSolver


core1 = PointKineticsSolver()

# Set starting neutrons
core1.set_neutrons(1E8)

# Run for 60 seconds to reach initial equilibrium
core1.solve(t_change=60, log_freq=0.1)

# Positive reactivity step, run for further 60 seconds
core1.set_rho(1E-3)
core1.solve(t_change=60, log_freq=0.1)

# Negative reactivity step, run for further 60 seconds
core1.set_rho(-1E-3)
core1.solve(t_change=60, log_freq=0.1)

# Back to zero reactivity (critical), run for further 60 seconds
core1.set_rho(0.0)
core1.solve(t_change=60, log_freq=0.1)

core1.plot_rho()
core1.plot_neutrons()
core1.plot_precursors()
