"""Class containing forward Euler ode"""


class ForwardEulerPC:
    """Perform the forward Euler method to progress a solution."""

    def __init__(self, ddt, h=1E-3):
        self.ddt = ddt
        self.h = h

    def solve(self, state_vect, t_target):
        """Progress the solution using the foward Euler method with
           trapezoidal predictor-corrector.

        Args:
            state_vect - current state of the system as a list.
            t_target - final time position.

        Returns:
            current_vect - current state of the system as a vector.

        Excepts:
            None"""

        current_vect = list(state_vect)

        while True:
            
            predictor_vect = [y+self.h*grad
                              for y,grad in zip(current_vect,
                                                self.ddt(current_vect),
                                               )
                             ]
            
            corrector_vect = [y + 0.5*self.h*(grad1 + grad2)
                              for y,grad1,grad2 in zip(current_vect,
                                                       self.ddt(current_vect),
                                                       self.ddt(predictor_vect)
                                                       )
                             ]
            
            current_vect = corrector_vect
            
            if current_vect[0] > t_target:
                return current_vect
