class PointKineticsConstants:
    
    betai_default = [0.000215, 0.001424, 0.001274, 0.002568, 0.000748, 0.000273]
    lambdai_default = [0.0124, 0.0305, 0.111, 0.301, 1.14, 3.01	]
    nGenTime_default = 1E-3
    
    def __init__(self,
                 betai = betai_default,
                 lambdai = lambdai_default,
                 nGenTime = nGenTime_default
                ):
        self.betai = betai
        self.lambdai = lambdai
        self.nGenTime = nGenTime
        self.beta = sum(betai)
        self.ndg = len(lambdai)
