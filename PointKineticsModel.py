class PointKineticsModel:
    """Class for the kinetics model."""

    def __init__(self, constants):

        self.constants = constants

    def d_by_dt(self, vector):
        """Calculates rate of change of precursors.

        Arguments:
            vector - list containing the initial value of the neutron
            population, the reactivity change made to the system, and the
            precursor values.

        Returns:
            dt_dt - the rate of change of time over time.
            dn_dt - the rate of change of population over time.
            drho_dt - rate of change of reactivity over time.
            dPrecursor_dt - amount contributed by the neutron energy group
            precursors to each of the above.

        Excepts:
            None"""

        neutron_population = vector[1]
        rho = vector[2]
        precursors = vector[3:]

        dt_dt = 1.0

        dn_dt = ((rho-self.constants.beta) *
                 neutron_population) / self.constants.nGenTime

        for i in range(self.constants.ndg):
            dn_dt += self.constants.lambdai[i] * precursors[i]

        drho_dt = 0.0

        dPrecursor_dt = [0.0] * self.constants.ndg

        for i in range(self.constants.ndg):
            dPrecursor_dt[i] = ((self.constants.betai[i]
                                 * neutron_population)
                                / self.constants.nGenTime)\
                    - (self.constants.lambdai[i]
                       * precursors[i])

        return [dt_dt, dn_dt, drho_dt] + dPrecursor_dt
