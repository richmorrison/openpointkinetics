class PointKineticsModel:
    
    def __init__(self, constants):
        
        self.constants = constants
    
    def dBydt(self, vector):
        
        n = vector[1]
        rho = vector[2]
        precursors = vector[3:]
        
        dtdt = 1.0
        
        dndt = (rho-self.constants.beta)*n/self.constants.nGenTime
        for i in range(self.constants.ndg):
            dndt +=self.constants.lambdai[i]*precursors[i]
        
        drhodt = 0.0
        
        dPrecdt = [0.0]*self.constants.ndg
        
        for i in range(self.constants.ndg):
            dPrecdt[i]=(self.constants.betai[i]*n/self.constants.nGenTime)-self.constants.lambdai[i]*precursors[i]
        
        return [dtdt, dndt, drhodt]+dPrecdt
