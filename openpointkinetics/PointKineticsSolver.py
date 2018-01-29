"""Point Kinetics Solver.

Point kinetics solver class. Feed it a power level via `set_power`, a
reactivity change via `set_rho`, and an amount of time and temporal resolution
over which to progress a solution via `solve`, and get access to plot
functionality for the data stored via these methods.
"""
from openpointkinetics.PointKineticsModel import PointKineticsModel
from openpointkinetics.PointKineticsConstants import PointKineticsConstants
from openpointkinetics.PointKineticsState import PointKineticsState
from openpointkinetics.Logger import Logger
from openpointkinetics.numericalmethods import Builder

class PointKineticsSolver:

    """Contains functionality to set reactivity parameters and solve for power
    and precursor populations.

    Args:
        constants - the constants required by the solver: the beta group
            coefficients; lambda group coefficients; the neutron generation
            time; the beta value; and the total number of groups. If nothing
            is provided to the solver, the defaults are taken from the
            PointKineticsConstants module.
        method - the method used by the solver, as dictated by an integer
            value. Currently the list of possible solvers is as follows:

                1: Forward Euler Method

            If no value is provided, the method will default to the Forward
            Euler Method.


    """

    def __init__(self, constants=None, method='F_Euler'):

        if constants is None:
            constants = PointKineticsConstants()

        self.logger1 = Logger()

        self.ndg = constants.ndg

        self.pk_model = PointKineticsModel(constants)

        self.state = PointKineticsState(constants.ndg)
        self.set_power(0.0)

        self.method = Builder.builder(method, lambda vector: self.pk_model.d_by_dt(vector))

    def set_power(self, power):
        """Set initial core power."""
        self.state.p = power

    def set_rho(self, rho):
        """Set reactivity at the current time."""
        self.state.rho = rho

    def add_rho(self, rho):
        """Create a reactivity addition."""
        self.state.rho = self.state.rho + rho

    def set_temperature(self, temp):
        """Set isothermal core temperature at the current time."""
        self.state.temperature = temp
    
    def set_demand(self, dem):
        """Set steam demand at the current time"""
        self.state.demand = dem
    
    def add_demand(self, dem):
        """Add to current steam demand"""
        self.state.demand = self.state.demand + dem
    
    def set_alphaT(self, aT):
        """Set isothermal temperature coefficient of reactivity"""
        self.state.alphaT = aT
    
    def set_heatCapacity(self, capacity):
        """Set heat capacity of thermal feedback body"""
        self.state.heatCapacity = capacity
    
    def set_precursors(self, precursors):
        """Provide new precursor values, if you want. Make sure the list you
        provide is the same length as length of the precursor list that was
        created in the constructor."""
    
        if len(precursors) is not len(self.state.precursors):
            print("Wrong vector length for set_precursors operation.")
            exit()
    
        self.state.precursors = precursors
    
    def set_example_thermal_params(self):
        
        # For fun, let's speculate on some values for Sizewell B,
        # we can calculate some rough data from the document
        # http://www.iaea.org/inis/collection/NCLCollectionStore/_Public/29/010/29010110.pdf
        
        # Set a bulk isothermal temperature of 300 C
        self.set_temperature(300.0)
        
        # Approximate the core to a mass of water with volume equal to the volume
        # of water in the primary circuit - 334.5 m^3 (1 m^3 = 1E6 cm^3).
        # Specific heat capacity of water is 4.1813 J.g^-1.K^-1 @ 100C (this will do)
        # Density of water is 1.0 g per cubic cm
        self.set_heatCapacity(334.5*1E6*4.1813)

        # Not sure what a representative alpha-T would be. Picking -2.5E-4 as
        # a rough right-order-of-magnitude value.
        self.set_alphaT(-2.5E-4)

        # Set the core demand to the steam power of 3500 MW
        self.set_demand(3500.0E6)

        # Set the core power to the same as the steam power of 3500 MW)
        self.set_power(3500.0E6)

        # Set initial reactivity
        self.set_rho(0.0)
    
    def solve(self, t_change, log_freq, log=True):
        """Progress the solver by t_change seconds, logging at log_freq
        intervals."""

        t_stop = self.state.get_t() + t_change

        if log_freq <= 0.0:
            log_freq = t_stop

        while self.state.get_t() <= t_stop:
            
            if log:
            
                self.logger1.log("power", self.state.get_t(), self.state.p)
                self.logger1.log("rho", self.state.get_t(), self.state.rho)
                self.logger1.log("temperature", self.state.get_t(), self.state.temperature)
                self.logger1.log("demand", self.state.get_t(), self.state.demand)
                self.logger1.log("alphaT", self.state.get_t(), self.state.alphaT)
                self.logger1.log("heatCapacity", self.state.get_t(), self.state.heatCapacity)
                
                for i in range(self.ndg):
                    self.logger1.log("precursor"+str(i),
                                     self.state.get_t(),
                                     self.state.precursors[i])

            new_state = self.method.solve(self.state.vectorise(),
                                          self.state.get_t()+log_freq)

            self.state.load_vector(new_state)
    
    def settle(self):
        
        """Run simulation for a period to reach equilibrium.
        Turns off logging and resets t to 0s"""
        
        self.solve(300, 0, log=False)
        self.state.zero_t()

    def plot_power(self):
        """Plot core power from time 0 to latest t_stop from `solve`
        method."""

        self.logger1.plot(["power"],
                          xlabel="Time(s)",
                          ylabel="power",
                          ylog=True,
                          title="Variation of Core Power with Time")

    def plot_rho(self):
        """Plot reactivity changes from time 0 to latest t_stop from `solve`
        method"""

        self.logger1.plot(["rho"],
                          xlabel="Time(s)",
                          ylabel="Rho",
                          title="Variation of Reactivity with Time")

    def plot_temperature(self):
        """Plot temperature changes from time 0 to latest t_stop from 'solve'"""
        
        self.logger1.plot(["temperature"],
                          xlabel="Time(s)",
                          ylabel="Temperature",
                          title="Variation of Temperature with Time")

    def plot_demand(self):
        """Plot steam demand changes from time 0 to latest t_stop from 'solve'"""
        
        self.logger1.plot(["demand"],
                          xlabel="Time(s)",
                          ylabel="Steam Demand (J)",
                          title="Variation of Steam Demand with Time")

    def plot_alphaT(self):
        """Plot alpha-T changes from time 0 to latest t_stop from 'solve'"""
        
        self.logger1.plot(["alphaT"],
                          xlabel="Time(s)",
                          ylabel="alpha-T",
                          title="Variation of alpha-T with Time")

    def plot_heatCapacity(self):
        """Plot changes in thermal body heat capacity from time 0 to latest t_stop from 'solve'"""
        
        self.logger1.plot(["heatCapacity"],
                          xlabel="Time(s)",
                          ylabel="Heat Capacity",
                          title="Variation of Thermal Body Heat Capacity with Time")

    def plot_precursors(self):
        """Plot precursor populations from time 0 to latest t_stop from `solve`
        method."""

        self.logger1.plot(["precursor"+str(i) for i in range(self.ndg)],
                          xlabel="Time(s)",
                          ylabel="Number in Group",
                          ylog=True,
                          title="Variation of Number of Delayed\
                            Neutron Precursors with Time")
