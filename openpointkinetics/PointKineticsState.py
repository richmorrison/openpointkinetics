"""Point Kinetics System State module."""


class PointKineticsState:
    """Set the state of the system."""

    def __init__(self, ndg):

        self.ndg = ndg  # number of delayed groups

        self.power = 0.0  # core power

        self.rho = 0.0  # core reactivity

        self.temperature = 0.0  # isothermal approximation of core temp

        self.demand = 0.0  # steam demand (Watts)

        """alpha_t could vary with time or state, so is not considered a
        constant and is best placed in this module (isothermal
        approximation)"""
        self.alpha_t = 0.0

        self.heat_capacity = 0.0  # of total thermal body (Joules/Kelvin)

        """List of precursor populations in each group. Since we are modelling
        power and not neutron numbers, "precursor population"" is to be
        interpreted as:

        energyPerFission*fissionCrossSection*actualPrecursorPopulation"""
        self.precursors = [0.0]*ndg

        self.time = 0.0

        self.vectorLen = self.ndg+7  # Length of system state when vectorised

    def vectorise(self):
        """Pack the separate paramers into a single list.

        Args:
            None

        Returns:
            vector - list made of time value, power, reactivity
                change, and all precursor values.

        Excepts:
            None"""

        vector = [0.0]*self.vectorLen

        vector[0] = self.time
        vector[1] = self.power
        vector[2] = self.rho
        vector[3] = self.temperature
        vector[4] = self.demand
        vector[5] = self.alpha_t
        vector[6] = self.heat_capacity
        vector[7:] = self.precursors

        return vector

    def load_vector(self, vector):
        """Pack the separate paramers into a single list."""

        if len(vector) is not self.vectorLen:
            print("Wrong vector length for vector load operation.")
            exit()

        self.time = vector[0]
        self.power = vector[1]
        self.rho = vector[2]
        self.temperature = vector[3]
        self.demand = vector[4]
        self.alpha_t = vector[5]
        self.heat_capacity = vector[6]
        self.precursors = vector[7:]

        return None

    def get_t(self):
        """Return current time value."""

        return self.time
    
    def zero_t(self):
        """Zero time value"""
        self.time = 0.0
