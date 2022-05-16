import ode_env
import numpy as np
from numpy.linalg import inv

class ErrorDynamics:

    def __init__(self, xEnv1, xEnv2, envT, sign):
        self.x1 = xEnv1
        self.x2 = xEnv2   
        self.envT = envT

        self.err = 0.0
        self.errDot = 0.0

        self.sign = sign
        # self.calcErr()
        
    def calcErr(self):
        self.prevErr = self.err

        x1 = self.x1.getX()
        x2 = self.x2.getX()

        self.err = x1 - x2
        if self.sign:
            self.err = -1.0 * self.err

        return self

    def calcErrDot(self):
       deltaT = self.envT.getDeltaT()
       self.errDot = (self.err - self.prevErr) / deltaT
       if self.sign:
           self.errDot = -1.0 * self.errDot

       return self

    def yieldStates(self):
        yield self.getErrDot()
        yield self.getErr()

    def getX(self):
        return self.err

    def getX1(self):
        return self.x1.getX()

    def getX2(self):
        return self.x2.getX()

    def getX1Dot(self):
        return self.x1.getXDot()

    def getX2Dot(self):
        return self.x2.getXDot()

    def getErr(self):
        return self.err

    def getErrDot(self):
        return self.errDot

    def getTransformed(self, lambdas):
        t = np.array([[1., 1.], [lambdas[0], lambdas[1]]])
        tInv = inv(t)
        e = np.array([self.err, self.errDot])
        eTrans = np.matmul(tInv, e)

        return eTrans

    def getTrans2Norm(self, lambdas):
        eTrans = self.getTransformed(lambdas)
        # debug
        # is it norm^2?
        norm = np.dot(eTrans, eTrans)
        # end of debug
        return norm

    def get2Norm2(self):
        self.calcErr()
        e = self.err
        norm = e * e

        return norm