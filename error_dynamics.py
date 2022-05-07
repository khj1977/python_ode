import ode_env

class ErrorDynamics:

    def __init__(self, xEnv1, xEnv2, envT):
        self.x1 = xEnv1
        self.x2 = xEnv2   
        self.envT = envT

        self.err = 0.0
        self.errDot = 0.0
        # self.calcErr()
        
    def calcErr(self):
        self.prevErr = self.err

        x1 = self.x1.getX()
        x2 = self.x2.getX()

        self.err = x1 - x2

        return self

    def calcErrDot(self):
       deltaT = self.envT.getDeltaT()
       self.errDot = (self.err - self.prevErr) / deltaT

       return self

    def yieldStates(self):
        yield self.getErrDot()
        yield self.getErr()

    def getX(self):
        return self.getX1()

    def getX1(self):
        return self.x1.getX()

    def getX2(self):
        return self.x1.getXDot()

    def getX1Dot(self):
        return self.x1.getXDot()

    def getX2Dot(self):
        return self.x2.getXDot()

    def getErr(self):
        return self.err

    def getErrDot(self):
        return self.errDot

    def get2Norm(self):
        self.calcErr()
        e = self.err
        norm = e * e

        return norm