#!/usr/bin/env python
"""Lesson 3 - Change steam demand"""
import openpointkinetics


# Create a new core
core1 = openpointkinetics.PointKineticsSolver()

core1.set_example_thermal_params()

# settle to equilibrium
core1.settle()

# 30 second lead time to start graph
core1.solve(t_change=30, log_freq=0.1)

# Core power is controlled by taking more steam from
# the plant. The resulting temperature change should cause a power increase
# and we should eventually return to the standard operating temperature.
core1.set_demand(4000.0E6)
core1.solve(t_change=300, log_freq=0.1)  # Give it 5 minutes to watch equilibrium evolve.

core1.plot_rho()
core1.plot_power()
core1.plot_precursors()
core1.plot_temperature()
