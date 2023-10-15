class ODEAnalogueSineSignal:
    def __init__(self):
        self.lambda1 = 0.0
        self.tau = 0.0
        self.t = 0.0
        set.envT = none
        # return self

    def setEnvT(self, envT):
        self.envT = envT
        return self

    def reset(self):
        self.tau = 0.0

        return self
    
    def isSin(self):
        pass

    def getLamnda(self):
        return self.lambda1