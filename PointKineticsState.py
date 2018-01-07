"""Point Kinetics System State module."""


class PointKineticsState:
    """Set the state of the system."""

    def __init__(self, ndg):

        self.ndg = ndg
        self.p = 0.0
        self.rho = 0.0

        self.precursors = [0.0]*ndg

        self.t = 0.0

        self.vectorLen = self.ndg+3

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

        vector[0] = self.t
        vector[1] = self.p
        vector[2] = self.rho
        vector[3:] = self.precursors

        return vector

    def load_vector(self, vector):
        """Pack the separate paramers into a single list."""

        if len(vector) is not self.vectorLen:
            print("Wrong vector length for vector load operation.")
            exit()

        self.t = vector[0]
        self.p = vector[1]
        self.rho = vector[2]
        self.precursors = vector[3:]

        return None

    def get_t(self):
        """Return current time value."""

        return self.t
