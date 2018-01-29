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

        self.method = Builder.builder(method, lambda vector:
                                      self.pk_model.d_by_dt(vector))

    def set_power(self, power):
        """Set initial core power."""
        self.state.power = power

    def set_rho(self, rho):
        """Set reactivity at the current time."""
        self.state.rho = rho

    def add_rho(self, rho):
        """Create a reactivity addition."""
        self.state.rho = self.state.rho + rho

    def set_temperature(self, temperaturej):
        """Set isothermal core temperature at the current time."""
        self.state.temperature = temperaturej

    def set_demand(self, demand):
        """Set steam demand at the current time"""
        self.state.demand = demand

    def add_demand(self, demand):
        """Add to current steam demand"""
        self.state.demand = self.state.demand + demand

    def set_alpha_t(self, alpha_t):
        """Set isothermal temperature coefficient of reactivity"""
        self.state.alpha_t = alpha_t

    def set_heat_capacity(self, heat_capacity):
        """Set heat capacity of thermal feedback body"""
        self.state.heat_capacity = heat_capacity

    def set_precursors(self, precursors):
        """Provide new precursor values, if you want. Make sure the list you
        provide is the same length as length of the precursor list that was
        created in the constructor."""

        if len(precursors) is not len(self.state.precursors):
            print("Wrong vector length for set_precursors operation.")
            exit()  # TODO: should this be 'return None'?

        self.state.precursors = precursors

    def solve(self, t_change, log_freq):
        """Progress the solver by t_change seconds, logging at log_freq
        intervals."""

        t_stop = self.state.get_t() + t_change

        if log_freq <= 0.0:
            log_freq = t_stop

        while self.state.get_t() <= t_stop:

            self.logger1.log("power", self.state.get_t(), self.state.power)
            self.logger1.log("rho", self.state.get_t(), self.state.rho)
            self.logger1.log("temperature", self.state.get_t(),
                             self.state.temperature)
            self.logger1.log("demand", self.state.get_t(), self.state.demand)
            self.logger1.log("alpha_t", self.state.get_t(), self.state.alpha_t)
            self.logger1.log("heat_capacity", self.state.get_t(),
                             self.state.heat_capacity)

            for i in range(self.ndg):
                self.logger1.log("precursor"+str(i),
                                 self.state.get_t(),
                                 self.state.precursors[i])

            new_state = self.method.solve(self.state.vectorise(),
                                          self.state.get_t()+log_freq)

            self.state.load_vector(new_state)

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
                          ylabel=r"$\rho$",
                          title="Variation of Reactivity with Time")

    def plot_temperature(self):
        """Plot temperature changes from time 0 to latest t_stop from
        'solve'"""

        self.logger1.plot(["temperature"],
                          xlabel="Time(s)",
                          ylabel="Temperature",
                          title="Variation of Temperature with Time")

    def plot_demand(self):
        """Plot steam demand changes from time 0 to latest t_stop from
        'solve'"""

        self.logger1.plot(["demand"],
                          xlabel="Time(s)",
                          ylabel="Steam Demand (J)",
                          title="Variation of Steam Demand with Time")

    def plot_alpha_t(self):
        """Plot alpha_t changes from time 0 to latest t_stop from 'solve'"""

        self.logger1.plot(["alpha_t"],
                          xlabel="Time(s)",
                          ylabel=r"$\alpha_{T}$",
                          title=r"Variation of $\alpha_{T}$ with Time")
    def plot_heat_capacity(self):
        """Plot changes in thermal body heat capacity from time 0 to latest
        t_stop from 'solve'"""

        self.logger1.plot(["heat_capacity"],
                          xlabel="Time(s)",
                          ylabel="Heat Capacity",
                          title="Variation of Thermal Body Heat\
                            Capacity with Time")

    def plot_precursors(self):
        """Plot precursor populations from time 0 to latest t_stop from `solve`
        method."""

        self.logger1.plot(["precursor"+str(i) for i in range(self.ndg)],
                          xlabel="Time(s)",
                          ylabel="Number in Group",
                          ylog=True,
                          title="Variation of Number of Delayed Neutron Precursors with Time")
