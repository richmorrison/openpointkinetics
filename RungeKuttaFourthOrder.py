"""Class containing the fourth-order Runge-Kutta method (RK4) ODE"""


class RK4:
    """Perform RK4 to progress a solution."""

    def __init__(self, ddt, h=1E-3):
        """Args:
            ddt - function
            h - step """
        self.ddt = ddt
        self.h = h

    def solve(self, state_vect, t_target):
        """Progress the solution using RK4.

        Args:
            state_vect - current state of the system as a list.
            t_target - final time position.

        Returns:
            current_vect - current state of the system as a vector.

        Excepts:
            None"""

        current_vect = list(state_vect)

        while True:
            t, y, *others = current_vect

            k1 = self.ddt([t] + [y] + others)
            k2 = self.ddt([t + self.h/2.] + [y + self.h*k1[1]/2.] + others)
            k3 = self.ddt([t + self.h/2.] + [y + self.h*k2[1]/2.] + others)
            k4 = self.ddt([t + self.h/2.] + [y + self.h*k3[1]] + others)

            current_vect = [y + (self.h/6.)*(k1 + 2*k2 + 2*k3 + k4)
                            for y, k1, k2, k3, k4
                            in zip(current_vect, k1, k2, k3, k4)]

            if current_vect[0] > t_target:
                return current_vect
