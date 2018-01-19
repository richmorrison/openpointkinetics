#!/usr/bin/python
"""Lesson 1 - Reactivity bump without thermal feedback"""
import openpointkinetics



core1 = openpointkinetics.PointKineticsSolver()

# Set starting neutrons
core1.set_power(1E8)

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
core1.plot_power()
core1.plot_precursors()
