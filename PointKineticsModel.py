"""Point Kinetics Model for progressing system."""


class PointKineticsModel:
    """Class for the kinetics model."""

    def __init__(self, constants):

        self.constants = constants

    def d_by_dt(self, vector):
        """Calculates rate of change of all elements of a vectorised state.

        Arguments:
            vector - list containing the current state variables of the
            system, as returned by a PointKineticsState instance.
            [t, power, rho, c1...cN]

        Returns:
            dt_dt - the rate of change of time over time.
            dp_dt - the rate of change of population over time.
            drho_dt - rate of change of reactivity over time.
            dPrecursor_dt - amount contributed by the neutron energy group
            precursors to each of the above.

        Excepts:
            None"""

        power = vector[1]
        rho = vector[2]
        temperature = vector[3]
        demand = vector[4]
        alphaT = vector[5]
        heatCapacity = vector[6]
        precursors = vector[7:]

        dt_dt = 1.0

        dp_dt = ( ((rho-self.constants.beta) / self.constants.n_gen_time) *
                 power )

        for i in range(self.constants.ndg):
            dp_dt += self.constants.lambda_groups[i] * precursors[i]

        dtemp_dt = (power - demand) / heatCapacity
        
        drho_dt = dtemp_dt * alphaT
        
        ddemand_dt = 0.0
        
        dalphaT_dt = 0.0
        
        dheatCapacity_dt = 0.0
        
        dPrecursor_dt = [0.0] * self.constants.ndg

        for i in range(self.constants.ndg):
            dPrecursor_dt[i] = ( (self.constants.beta_groups[i] / 
                                 self.constants.n_gen_time) *
                                 power -
                                 (self.constants.lambda_groups[i] *
                                 precursors[i]) )

        return [dt_dt,
                dp_dt,
                drho_dt,
                dtemp_dt,
                ddemand_dt,
                dalphaT_dt,
                dheatCapacity_dt ] + dPrecursor_dt
