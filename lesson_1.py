#!/usr/bin/env python
"""Lesson 1 - Reactivity bump without thermal feedback"""
import openpointkinetics


core1 = openpointkinetics.PointKineticsSolver()

core1.set_power(1E8)  # Set starting neutrons

core1.solve(t_change=60, log_freq=0.1)  # 60s run for initial equilibrium

core1.set_rho(1E-3)  # positive reactivity step
core1.solve(t_change=60, log_freq=0.1)  # run for another 60s

core1.set_rho(-1E-3)  # negative reactivity step
core1.solve(t_change=60, log_freq=0.1)  # run for another 60s

core1.set_rho(0.0)  # back to 0 (critical)
core1.solve(t_change=60, log_freq=0.1)  # run for another 60s

core1.plot_rho()
core1.plot_power()
core1.plot_precursors()
