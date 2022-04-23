import ode_env

class ErrorDynamics:

    def __init__(self, xEnv1, xEnv2):
        self.x1 = xEnv1
        self.x2 = xEnv2   
        self.calcErr()
        
    def calcErr(self):
        x1 = self.x1.getX()
        x2 = self.x2.getX()

        self.err = x1 - x2

        return self

    def yieldStates(self):
        yield self.x1
        yield self.x2

    def getX1(self):
        return self.x1

    def getX2(self):
        return self.x2

    def getX1Dot(self):
        return self.x1.getXDot()

    def getX2Dot(self):
        return self.x2.getXDot()

    def get2Norm(self):
        self.calcErr()
        e = self.err
        norm = e * e

        return norm