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
                power - power of the plant, expressed as the number of neutrons
                in the system.
                rho - reactivity of the system
                temperature - temperature of the system
                demand - steam demand of teh system
                alpha_t - temperature coefficient of reactivity, i.e. how the
                reactivity changes with temperature
                heat_capacity - heat capacity of the system
                precursors - information about the precursors

        Returns:
            dt_dt - rate of change of time over time
            dp_dt - rate of change of population over time
            drho_dt - rate of change of reactivity over time
            dtemp_dt - rate of change of temperature
            ddemand_dt - rate of change of steam demand
            dalpha_t_dt - rate of change of temperature coefficient of
                reactivity
            dheat_capacity_dt - rate of change of heat capacity
            dprecursor_dt - rate of change of all precursors

            all of the above is the differential with respect to time

        Excepts:
            None"""

        power = vector[1]
        rho = vector[2]
        temperature = vector[3]  # unused but kept for readability
        demand = vector[4]
        alpha_t = vector[5]
        heat_capacity = vector[6]
        precursors = vector[7:]

        dt_dt = 1.0

        dp_dt = (((rho-self.constants.beta) / self.constants.n_gen_time) *
                 power)

        for i in range(self.constants.ndg):
            dp_dt += self.constants.lambda_groups[i] * precursors[i]
        if heat_capacity <= 0:
            dtemp_dt = 0.0
        else:
            dtemp_dt = (power - demand) / heat_capacity

        drho_dt = dtemp_dt * alpha_t
        ddemand_dt = 0.0

        dalpha_t_dt = 0.0

        dheat_capacity_dt = 0.0

        dprecursor_dt = [0.0] * self.constants.ndg

        for i in range(self.constants.ndg):
            dprecursor_dt[i] = ((self.constants.beta_groups[i] /
                                 self.constants.n_gen_time) *
                                 power -
                                 (self.constants.lambda_groups[i] *
                                 precursors[i]) )

        return [dt_dt, dp_dt, drho_dt, dtemp_dt, ddemand_dt, dalphaT_dt,
                dheatCapacity_dt] + dPrecursor_dt
