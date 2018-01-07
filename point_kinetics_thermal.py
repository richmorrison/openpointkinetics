#!/usr/bin/python
"""Example use of the PointKineticsSolver"""

from PointKineticsSolver import PointKineticsSolver


# Create a new core
core1 = PointKineticsSolver()

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
# a right-order-of-magnitude value.
core1.set_alphaT(-2.5E-4)

# Set the core demand to the steam power of 3500 MW
core1.set_demand(3500.0E6)

# Set the core power to the same as the steam power of 3500 MW)
core1.set_power(3500.0E6)

# Set initial reactivity.
core1.set_rho(0.0)

# Half-hour simulated time
core1.solve(t_change=1800, log_freq=0.1)

core1.plot_rho()
core1.plot_power()
core1.plot_precursors()
core1.plot_temperature()
