class DeltaLambda:

    # debug
    # choose f or g based on lyapunov value. set omega and delta.
    # set tau as actual num which is current time for start.
    # capule those info to objects and make method lambdaUncrementer->exec()
    # end of debug
    def __init__(self, envT):
        self.envT = envT

        self.calcF = lambda x: x
        self.calcG = lambda x: x + 1

        delta = self.getDelta()
        self.calcH = lambda x: -1.0 * delta
        self.calcQ = lambda x: 0.0

        self.lambdaDot = self.calcH

        pass

    def inc(self):
        pass

    def getDeltaLambda(self);
        pass

    def getLambda(self):
        pass

    def setOmega(self, omega):
        pass

    def setTau(self, tau):
        pass
