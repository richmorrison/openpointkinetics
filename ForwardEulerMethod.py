"""Class containing forward Euler ode"""


class ForwardEulerMethod:
    """Perform the forward Euler method to progress a solution."""

    def __init__(self, ddt, h=1E-3):
        self.ddt = ddt
        self.h = h

    def solve(self, state_vect, t_target):
        """Progress the solution using the foward Euler method.

        Args:
            state_vect - current state of the system as a list.
            t_target - final time position.

        Returns:
            current_vect - current state of the system as a vector.

        Excepts:
            None"""

        current_vect = list(state_vect)

        while True:
            grad_vect = self.ddt(current_vect)

            current_vect = [y+self.h*grad
                            for y, grad in zip(current_vect, grad_vect)]

            if current_vect[0] > t_target:
                return current_vect
