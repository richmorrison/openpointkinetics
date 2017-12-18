"""Point Kinetics Solver.

Point kinetics solver class. Feed it a number of neutrons via `set_neutrons`, a
reactivity change via `set_rho`, and an amount of time and tempoeral resolution
over which to progress a solution via `solve`, and get access to plot
functionality for the data stored via these methods.
"""
from PointKineticsModel import PointKineticsModel
from PointKineticsConstants import PointKineticsConstants
from PointKineticsState import PointKineticsState
from ForwardEulerMethod import ForwardEulerMethod
from Logger import Logger


class PointKineticsSolver:

    """Contains functionality to set reactivity parameters and solve for neutron
    population and precursor populations.

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

    def __init__(self, constants=None, method=1):

        if constants is None:
            constants = PointKineticsConstants()

        self.logger1 = Logger()

        self.ndg = constants.ndg

        self.pk_model = PointKineticsModel(constants)

        self.state = PointKineticsState(constants.ndg)
        self.set_neutrons(0.0)

        if method is 1:
            self.method = ForwardEulerMethod(lambda vector:
                                             self.pk_model.d_by_dt(vector))

    def set_neutrons(self, neutrons):
        """Set initial neutron population."""
        self.state.n = neutrons

    def set_rho(self, rho):
        """Set reactivity change at the current time in the solver."""
        self.state.rho = rho

    def add_rho(self, rho):
        """Create a reactivity addition."""
        self.state.rho = self.state.rho + rho

    def set_precursors(self, precursors):
        """Provide new precursor values, if you want. Make sure the list you
        provide is the same length as length of the precursor list that was
        created in the constructor."""

        if len(precursors) is not len(self.state.precursors):
            print("Wrong vector length for set_precursors operation.")
            exit()

        self.state.precursors = precursors

    def solve(self, t_stop, log_freq):
        """Progress the solver to the stop time t_stop logging at log_freq
        intervals."""

        if log_freq <= 0.0:
            log_freq = t_stop

        while self.state.get_t() <= t_stop:

            self.logger1.log("neutrons", self.state.get_t(), self.state.n)
            self.logger1.log("rho", self.state.get_t(), self.state.rho)

            for i in range(self.ndg):
                self.logger1.log("precursor"+str(i),
                                 self.state.get_t(),
                                 self.state.precursors[i])

            new_state = self.method.solve(self.state.vectorise(),
                                          self.state.get_t()+log_freq)

            self.state.load_vector(new_state)

    def plot_neutrons(self):
        """Plot neutron population from time 0 to latest t_stop from `solve`
        method."""

        self.logger1.plot(["neutrons"],
                          xlabel="Time(s)",
                          ylabel="Neutrons",
                          ylog=True,
                          title="Variation of Number of Neutrons with Time")

    def plot_rho(self):
        """Plot reactivity changes from time 0 to latest t_stop from `solve`
        method"""

        self.logger1.plot(["rho"],
                          xlabel="Time(s)",
                          ylabel="Rho",
                          title="Variation of Reactivity with Time")

    def plot_precursors(self):
        """Plot precursor populations from time 0 to latest t_stop from `solve`
        method."""

        self.logger1.plot(["precursor"+str(i) for i in range(self.ndg)],
                          xlabel="Time(s)",
                          ylabel="Number in Group",
                          ylog=True,
                          title="Variation of Number of Delayed\
                            Neutron Precursors with Time")
