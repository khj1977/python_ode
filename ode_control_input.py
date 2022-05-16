class ControlInput:
    def __init__(self):
        self.u = 0.0
        self.prevU = 0.0
        # return self
    
    def getControlInput(self):
        return self.u

    def getControlInputDot(self):
        deltaT = self.envT.getDeltaT()
        return (self.u - self.prevU) / deltaT

    def getStates(self):
        return self.env

    def setState(self, env):
        self.env = env

        return self

    # generally for nonlinear time varying control input.
    def setEnvT(self, envT):
        self.envT = envT
        return self

    def setCoef(self, coefs):
        self.coefs = coefs
        return self

    def getCoef(self):
        return self.coefs

    def setControlInput(self, controlInput):
        self.u = controlInput

        return self

    # linear control input which is a * x where they are vector.
    def calcControlInput(self):
        # debug
        # implement this method
        # determine linear control input based on coefs and state
        self.prevU = self.u
        u = 0.0
        for x in self.env.yieldStates():
            for a in self.coefs.yieldCoefs():
                u = u + a * x

        self.setControlInput(u)
        return self
        # end of debug
 
