class NullControlInput:
    def __init__(self):
        self.u = 0.0
        self.prevU = 0.0
        # return self
        
    def setDisturbance(self, estimatedDisturbance):
        self.estimatedDisturbance = estimatedDisturbance
        return self
    
    def getControlInput(self):
        return 0.0
        # return -1.0 * self.estimatedDisturbance.getControlInput()

    def getControlInputDot(self):
        deltaT = self.envT.getDeltaT()
        return (self.u - self.prevU) / deltaT

    def getStates(self):
        raise

    def setState(self, env):
        raise

    # generally for nonlinear time varying control input.
    def setEnvT(self, envT):
        self.envT = envT
        return self

    def setCoef(self, coefs):
        raise

    def getCoef(self):
        raise

    def setControlInput(self, disturbance):
        self.u = -1.0 * disturbance

        return self

    # linear control input which is a * x where they are vector.
    def calcControlInput(self):
        self.prevU = self.u
        self.u = -1.0 * self.estimatedDisturbance.getControlInput()
        return self
        # end of debug
 
