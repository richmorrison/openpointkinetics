class ForwardEulerMethod:
    
    def __init__(self, ddt, h=1E-3):
        self.h = h
        self.ddt = ddt
        
    def solve(self, stateVect, t_target):
        
        currentVect = list(stateVect)
        
        while True:
            gradVect = self.ddt(currentVect)
            currentVect = [y+self.h*grad for y,grad in zip(currentVect, gradVect)]
            if currentVect[0] > t_target:
                return currentVect


