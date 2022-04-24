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

        self.xddot = self.eq(t, self.x, self.xDot)

        return self.xddot
    # end of debug

    def getStates(self):
        # debug
        # the following is mistake. Implment appropriate one
        return [self.envT.getT(), self.x, self.xDot]
        # end of debug