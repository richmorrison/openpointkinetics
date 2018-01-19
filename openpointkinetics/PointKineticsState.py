"""Point Kinetics System State module."""


class PointKineticsState:
    """Set the state of the system."""

    def __init__(self, ndg):

        # Number of delayed groups
        #
        self.ndg = ndg
        
        # Core power
        #
        self.p = 0.0
        
        # Core reactivity
        #
        self.rho = 0.0
        
        # Temperature of the core (isothermal approximation)
        #
        self.temperature = 0.0
        
        # Steam demand on the core (Watts)
        #
        self.demand = 0.0
        
        # alphaT could vary with time or state, so is not considered a constant
        # and is best placed in this module
        # (isothermal approximation)
        #
        self.alphaT = 0.0
        
        # Heat capacity of total thermal body (J/K)
        self.heatCapacity = 0.0
        
        # List of precursor populations in each group
        # Since we are modelling power and not neutron numbers,
        # "precursor population"" is to be interpreted as:
        #
        # energyPerFission*fissionCrossSection*actualPrecursorPopulation
        # 
        self.precursors = [0.0]*ndg

        # Time stamp of this state
        self.time = 0.0

        # Length of this state when vectorised
        self.vectorLen = self.ndg+7

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
        vector[1] = self.p
        vector[2] = self.rho
        vector[3] = self.temperature
        vector[4] = self.demand
        vector[5] = self.alphaT
        vector[6] = self.heatCapacity
        vector[7:] = self.precursors

        return vector

    def load_vector(self, vector):
        """Pack the separate paramers into a single list."""

        if len(vector) is not self.vectorLen:
            print("Wrong vector length for vector load operation.")
            exit()

        self.time = vector[0]
        self.p = vector[1]
        self.rho = vector[2]
        self.temperature = vector[3]
        self.demand = vector[4]
        self.alphaT = vector[5]
        self.heatCapacity = vector[6]
        self.precursors = vector[7:]

        return None

    def get_t(self):
        """Return current time value."""

        return self.time
