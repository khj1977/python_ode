import math

class DeltaLambda:

    # debug
    # choose f or g based on lyapunov value. set omega and delta.
    # set tau as actual num which is current time for start.
    # capule those info to objects and make method lambdaUncrementer->exec()
    # end of debug
    def __init__(self, envT, errorDynamics, delta, omega, tau):
        self.envT = envT
        self.errorDynamics = errorDynamics

        self.setDelta(delta)
        self.setOmega(omega)
        self.setTau(tau)

        self.calcF = lambda x: x
        def calcG(t): 
            if (t <= math.pi / omega + tau):
                1.0 / 2.0 * delta * math.sin(omega * (t - tau) + 3.0/2.0 * math.pi) - 1.0 / 2.0 * delta
            else:
                0.0
        
        self.calcG = calcG
       
        self.calcH = lambda x: -1.0 * delta
        self.calcQ = lambda x: 0.0

        self.lambdaDot = self.calcH

        pass

    def inc(self):
        pass

    def getDeltaLambda(self):
        pass

    def setDelta(self, delta):
        self.delta = delta

        return self

    def setOmega(self, omega):
        self.omega = omega

        return self

    def setTau(self, tau):
        self.tau = tau

        return self
