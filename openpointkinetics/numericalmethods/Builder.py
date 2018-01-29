"""Numerical Methods Factory.

Factory method to instantiate numerical methods classes. The intent here 
is the remove if..elif.. methods from the higher level solver class and
keep that code as tidy as possible.
"""


def builder(method, ddt, h=1E-3):

    from openpointkinetics.numericalmethods.ForwardEulerMethod import ForwardEulerMethod
    from openpointkinetics.numericalmethods.RungeKuttaFourthOrder import RK4

    # Set a default if the specified method not recognised
    if method.lower() not in [i.lower() for i in ['F_Euler', 'RK4']]:
        print("Unrecognised numerical method request passed to\
              NumericalMethodBuilder")
        print("Using default Forward-Euler method")
        method = 'F_Euler'

    if method.lower() == 'F_Euler'.lower():
        print("Using Forward-Euler method")
        return ForwardEulerMethod(ddt, h)

    elif method.lower() == 'RK4'.lower():
        print("Using Runge-Kutta method")
        return RK4(ddt, h)
