import math

class DeltaLambda:

    # debug
    # choose f or g based on lyapunov value. set omega and delta.
    # set tau as actual num which is current time for start.
    # capule those info to objects and make method lambdaUncrementer->exec()
    # end of debug
    def __init__(self, envT, errorDynamics, delta, omega, tau, epsilon):
        self.envT = envT
        self.errorDynamics = errorDynamics

        self.setDelta(delta)
        self.setOmega(omega)
        self.setTau(tau)
        self.setEpsilon(epsilon)

        self.calcF = lambda x: x
        
        def calcG(t, that): 
            if (t <= math.pi / omega + tau):
                that.setIsDelta(True)
                1.0 / 2.0 * delta * math.sin(omega * (t - tau) + 3.0/2.0 * math.pi) - 1.0 / 2.0 * delta
            else:
                that.setIsDelta(False)
                0.0
        
        self.calcG = calcG
       
        self.calcH = lambda x: -1.0 * delta
        self.calcQ = lambda x: 0.0

        self.lambdaDot = self.calcH

        self.innerFunc = self.calcQ

    def inc(self, lambdas):
        self.lyapunovValue = self.errorDynamics.getTrans2Norm(lambdas)
        e2 = self.epsilon * self.epsilon

        if self.lyapunovValue <= e2 and self.getIsDelta():
            self.innerFunc = self.calcF
        elif self.lyapunovValue > e2 and not(self.getIsDelta()):
            self.innerFunc = self.calcG
        else:
            self.innerFunc = self.calcQ


    def getDeltaLambda(self):
        pass

    def setIsDelta(self, flag):
        self.ifDelta = flag

        return self
    
    def getIsDelta(self):
        return self.isDelta

    def setDelta(self, delta):
        self.delta = delta

        return self

    def setOmega(self, omega):
        self.omega = omega

        return self

    def setTau(self, tau):
        self.tau = tau

        return self

    def setEpsilon(self, e):
        self.epsilon = e

        return self