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
        
        while current_vect[0] < t_target:
            
            k1 = self.ddt(current_vect)
            k2 = self.ddt( [current_vect[i]+self.h*(k1[i]/2) for i in range(len(current_vect))] )
            k3 = self.ddt( [current_vect[i]+self.h*(k2[i]/2) for i in range(len(current_vect))] )
            k4 = self.ddt( [current_vect[i]+self.h*k3[i]   for i in range(len(current_vect))] )
            
            current_vect=[current_vect[i]+(self.h/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(len(current_vect))]
            
        return current_vect
