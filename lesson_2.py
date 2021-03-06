#!/usr/bin/env python
"""Lesson 2 - Reactivity addition with thermal feedback"""
import openpointkinetics


core1 = openpointkinetics.PointKineticsSolver()  # create a new core

"""For fun, let's speculate on some values for Sizewell B,
we can calculate some rough data from the document
http://www.iaea.org/inis/collection/NCLCollectionStore/_Public/29/010/29010110.pdf"""
core1.set_temperature(300.0)  # set bulk isothermal temperature of 300C

"""Approximate the core to a mass of water with volume equal to the volume of
water in the primary circuit - 334.5 m^3 (1 m^3 = 1E6 cm^3). Specific heat
capacity of water is 4.1813 J.g^-1.K^-1 @ 100C (this will do) Density of water
is 1.0 g per cubic cm"""
core1.set_heat_capacity(334.5*1E6*4.1813)

"""Not sure what a representative alpha_t would be. Picking -2.5E-4 as a rough
right-order-of-magnitude value."""
core1.set_alpha_t(-2.5E-4)

core1.set_demand(3500.0E6)  # set the core demand to the steam power of 3500MW

core1.set_power(3500.0E6)  # set core power equal to steam demand

core1.set_rho(0.0)  # set rho (only do set_rho() once or it gets confused)

core1.settle()  # settle to equilibrium

core1.solve(t_change=30, log_freq=0.1)  # 30 second lead time to start graph

"""Let's suppose we raise the control rods and inject some reactivity without
changing the steam demand. We should see a self correcting power transient,
self-limited by a change in temperature. This means that operationally the rods
can be used to control core temperature, rather than power."""
core1.add_rho(1E-3)
core1.solve(t_change=300, log_freq=0.1)  # 5mins to establish some equilibrium

core1.plot_rho()
core1.plot_power()
core1.plot_precursors()
core1.plot_temperature()
