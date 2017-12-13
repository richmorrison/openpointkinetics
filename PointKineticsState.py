class PointKineticsState:
    
    
    def __init__(self, ndg):
        
        self.ndg = ndg
        self.n = 0.0
        self.rho = 0.0
        
        self.precursors = [0.0]*ndg
        
        self.t = 0.0
        
        self.vectorLen = self.ndg+3
    
    def vectorise(self):
        
        vector = [0.0]*self.vectorLen
        
        vector[0] = self.t
        vector[1] = self.n
        vector[2] = self.rho
        vector[3:] = self.precursors
        
        return vector
    
    def load_vector(self, vector):
        
        if len(vector) is not self.vectorLen:
            print("Wrong vector length for vector load operation.")
            exit()
        
        self.t = vector[0]
        self.n = vector[1]
        self.rho = vector[2]
        self.precursors=vector[3:]
        
        return
    
    def get_t(self):
        return self.t
    

