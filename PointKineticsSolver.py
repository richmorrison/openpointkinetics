from PointKineticsModel import *
from PointKineticsConstants import *
from PointKineticsState import *
from ForwardEulerMethod import *
from Logger import *

class PointKineticsSolver:
    
    
    def __init__(self, constants=None, method=1):
        
        if constants is None: constants = PointKineticsConstants()
        
        self.logger1 = Logger()
        
        self.ndg = constants.ndg
        
        self.pkModel = PointKineticsModel(constants)
        
        self.state = PointKineticsState(constants.ndg)
        self.set_neutrons(0.0)
        
        if method is 1:
            self.method=ForwardEulerMethod(
                lambda vector: self.pkModel.dBydt(vector)
            )
    
    def set_neutrons(self, neutrons):
        self.state.n = neutrons
    
    def set_rho(self, rho):
        self.state.rho = rho
    
    def set_precursors(self, precursors):
    
        if len(precursors) is not len(self.state.precursors):
            print("Wrong vector length for set_precursors operation.")
            exit()
        
        self.state.precursors = precursors
    
    def solve(self, t_stop, log_freq):
        
        if log_freq <= 0.0: log_freq = t_stop
        while self.state.get_t() <= t_stop:
        
            self.logger1.log("neutrons", self.state.get_t(), self.state.n)
            self.logger1.log("rho", self.state.get_t(), self.state.rho)
            
            for i in range(self.ndg):
                self.logger1.log("precursor"+str(i), self.state.get_t(), self.state.precursors[i])
            
            newState = self.method.solve(
                           self.state.vectorise(),
                           self.state.get_t()+log_freq
                       )
            self.state.load_vector(newState)
    
    def plot_neutrons(self):
        
        self.logger1.plot(
                          ["neutrons"],
                          xlabel="Time(s)",
                          ylabel="Neutrons",
                          ylog=True,
                          title="Variation of Number of Neutrons with Time"
                         )
                         
    def plot_rho(self):
        
        self.logger1.plot(
                          ["rho"],
                          xlabel="Time(s)",
                          ylabel="Rho",
                          title="Variation of Reactivity with Time"
                         )
    
    def plot_precursors(self):
        
        self.logger1.plot(
                          ["precursor"+str(i) for i in range(self.ndg)],
                          xlabel="Time(s)",
                          ylabel="Number in Group",
                          ylog=True,
                          title="Variation of Number of Delayed Neutron Precursors with Time"
                         )
