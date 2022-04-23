class ControlInput:
    def __init__(self):
        self.u = 0.0
        # return self
    
    def getControlInput(self):
        return self.u

    def getState(self):
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

    def setControlInput(self, controlInput):
        self.u = ControlInput

        return self

    # linear control input which is a * x where they are vector.
    def calcControlInput(self):
        # debug
        # implement this method
        # determine linear control input based on coefs and state
        u = 0.0
        for x in self.getControlInput.yieldState():
            for a in self.coefs.yieldCoefs():
                u = u + x * a

        self.setControlInput(u)
        return self
        # end of debug
 
