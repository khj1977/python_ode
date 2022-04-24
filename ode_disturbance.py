class Disturbance:
    def __init__(self, eq, envX, envT):
        self.eq = eq
        self.envX = envX
        self.envT = envT

    # debug
    # implement the following method.
    def getDynamics(self):
        x = self.envX.getX()
        xDot = self.envX.getXDot()
        t = self.envT.getT()

        val = self.eq(t, x, xDot)

        return val
    # end of debug