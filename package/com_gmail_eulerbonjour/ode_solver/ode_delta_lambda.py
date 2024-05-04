import math

class DeltaLambda:

    # debug
    # choose f or g based on lyapunov value. set omega and delta.
    # set tau as actual num which is current time for start.
    # capule those info to objects and make method lambdaUncrementer->exec()
    # end of debug
    def __init__(self, envT, errorDynamics, delta, omega, epsilon):
        self.envT = envT
        self.errorDynamics = errorDynamics

        self.setDelta(delta)
        self.setOmega(omega)
        # self.setTau(tau)
        self.setEpsilon(epsilon)

        self.setIsDelta(False)

        self.setTau(0.0)

        self.setPrevDelta(0.0)


        def calcF(t, tau, delta, that):
            # print("calc-f")
            if (t <= math.pi / omega + tau):
                that.setIsDelta(True)
                d =  1.0 / 2.0 * delta * math.sin(omega * (t - that.getTau()) + 3.0 / 2,0 * math.pi) - 1.0 / 2.0 * delta
                self.setPrevDelta(d)
                #p rint("foo1")
            else:
                that.setIsDelta(False)
                d = 0.0
                self.setPrevDelta(d)
                # print("foo2")

            # print(d)
            # print("\n")

            return d

        self.calcF = calcF
        
        def calcG(t, tau, delta, that): 
            # print("calc-g")
            if (t <= math.pi / omega + tau):
                that.setIsDelta(False)
                d = 1.0 / 2.0 * delta * math.sin(omega * (t - that.getTau()) + 1.0/2.0 * math.pi) - 1.0 / 2.0 * delta
                self.setPrevDelta(d)
                # print(math.pi / omega + tau)
                # print(t)
                # print("bar1")
            else:
                that.setIsDelta(True)
                d = 1.0 * delta
                self.setPrevDelta(d)
                # print(t)
                # print("bar2")

            # print(d)
            # print("\n")

            return d
        
        self.calcG = calcG
       
        self.calcQ = lambda x, y, w, that: that.getPrevDelta()

        # self.lambdaDot = self.calcH

        self.innerFunc = self.calcQ

    def inc(self, lambdas):
        self.lyapunovValue = self.errorDynamics.getTrans2Norm(lambdas)
        e2 = self.epsilon * self.epsilon

        # if self.lyapunovValue <= e2 and self.getIsDelta():
        if self.lyapunovValue <= e2 and self.getIsDelta():
            if not(self.getIsDelta()):
                self.setTau(self.envT.get())
            self.innerFunc = self.calcF
        elif self.lyapunovValue > e2 and not(self.getIsDelta()):
        # elif self.lyapunovValue > e2:
            if self.getIsDelta():
                self.setTau(self.envT.getT())
            self.innerFunc = self.calcG
        else:
            # print("calc-q")
            self.innerFunc = self.calcQ

        # print(self.getIsDelta())


    def getDeltaLambda(self):
        # print("delta: " + str(self.getDelta()))
        d = self.innerFunc(self.envT.getT(), self.getTau(), self.getDelta(), self)
        # print("d2: " + str(d))

        return d

    def setIsDelta(self, flag):
        self.isDelta = flag

        return self
    
    def getIsDelta(self):
        return self.isDelta

    def setDelta(self, delta):
        self.delta = delta

        return self
    
    def getDelta(self):
        return self.delta

    def setOmega(self, omega):
        self.omega = omega

        return self

    def setTau(self, tau):
        self.tau = tau

        return self
    
    def getTau(self):
        return self.tau

    def setEpsilon(self, e):
        self.epsilon = e

        return self
    
    def setPrevDelta(self, prevDelta):
        self.prevDelta = prevDelta

        return self

    def getPrevDelta(self):
        return self.prevDelta