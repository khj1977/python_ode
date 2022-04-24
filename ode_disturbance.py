class Disturbance:
    def __init__(self, eq, envX, envT):
        self.eq = eq
        self.envX = envX
        self.envT = envT

    # debug
    # implement the following method.
    def getDynamics(self):
        self.x = self.envX.getX()
        self.xDot = self.envX.getXDot()
        t = self.envT.getT()

        val = self.eq(t, self.x, self.xDot)

        return val
    # end of debug

    def getStates(self):
        return [self.envT.getT(), self.x, self.xDot]