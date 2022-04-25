class Disturbance:
    def __init__(self, eq, envX, envT):
        self.eq = eq
        self.envX = envX
        self.envT = envT
        self.disturbance = 0.0
        self.disturbanceDot = 0.0
        self.prevDisturbance = 0.0

    # debug
    # implement the following method.
    def calcDynamics(self):
        self.x = self.envX.getX()
        self.xDot = self.envX.getXDot()
        t = self.envT.getT()

        self.prevDisturbance = self.disturbance
        self.disturbance = self.eq(t, self.x, self.xDot)

        return self.disturbance
    # end of debug

    def calcDisturbanceDot(self):
        # self.prevDisturbance = self.disturbance
        # debug
        # self.calcDynamics(t)
        # end of debug
        diff = self.disturbance - self.prevDisturbance
        deltaT = self.envT.getDeltaT()
        disturbanceDot = diff / deltaT
        self.disturbanceDot = disturbanceDot

        return self

    def getStates(self):
        # debug
        # the following is mistake. Implment appropriate one
        return [self.envT.getT(), self.disturbance, self.disturbanceDot]
        # end of debug