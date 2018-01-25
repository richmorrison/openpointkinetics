class PointKineticsConstants:
    """Container for the physics constants relevant to the solver."""

    BETA_GROUPS = [0.000215,  # fractional yields for each group
                   0.001424,
                   0.001274,
                   0.002568,
                   0.000748,
                   0.000273]

    LAMBDA_GROUPS = [0.0124,  # decay constants for each group
                     0.0305,
                     0.111,
                     0.301,
                     1.14,
                     3.01]

    N_GEN_TIME = 1E-3  # neutron generation time

    def __init__(self, beta_groups=BETA_GROUPS, lambda_groups=LAMBDA_GROUPS,
                 n_gen_time=N_GEN_TIME):

        self.beta_groups = beta_groups
        self.lambda_groups = lambda_groups
        self.n_gen_time = n_gen_time
        self.beta = sum(beta_groups)
        self.ndg = len(lambda_groups)
