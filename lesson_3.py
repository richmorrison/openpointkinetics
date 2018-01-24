#!/usr/bin/env python
"""Lesson 3 - Change steam demand"""
import openpointkinetics


# Create a new core
core1 = openpointkinetics.PointKineticsSolver()

# For fun, let's speculate on some values for Sizewell B,
# we can calculate some rough data from the document
# http://www.iaea.org/inis/collection/NCLCollectionStore/_Public/29/010/29010110.pdf

# Set a bulk isothermal temperature of 300 C
core1.set_temperature(300.0)

# Approximate the core to a mass of water with volume equal to the volume
# of water in the primary circuit - 334.5 m^3 (1 m^3 = 1E6 cm^3).
# Specific heat capacity of water is 4.1813 J.g^-1.K^-1 @ 100C (this will do)
# Density of water is 1.0 g per cubic cm
core1.set_heatCapacity(334.5*1E6*4.1813)

# Not sure what a representative alpha-T would be. Picking -2.5E-4 as
# a rough right-order-of-magnitude value.
core1.set_alphaT(-2.5E-4)

# Set the core demand to the steam power of 3500 MW
core1.set_demand(3500.0E6)

# Set the core power to the same as the steam power of 3500 MW)
core1.set_power(3500.0E6)

# Set initial reactivity (Only do set_rho() once or things get confused)
core1.set_rho(0.0)

# 5 mins to settle
core1.solve(t_change=300, log_freq=0.1)

# Core power is controlled by taking more steam from
# the plant. The resulting temperature change should cause a power increase
# and we should eventually return to the standard operating temperature.
core1.set_demand(4000.0E6)
core1.solve(t_change=300, log_freq=0.1) # Give it 5 minutes to watch equilibrium evolve.

core1.plot_rho()
core1.plot_power()
core1.plot_precursors()
core1.plot_temperature()
