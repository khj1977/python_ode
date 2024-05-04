from numpy import true_divide


class ODETime:
    def __init__(self, startT, endT, deltaT):
        self.t = startT
        self.startT = startT
        self.endT = endT
        self.deltaT = deltaT

    def startClock(self):
        while True:
            if self.t > self.endT:
                break
            self.t = self.t + self.deltaT
            yield self.t
            
        return self

    def setT(self, t):
        self.t = t
        return self

    def getT(self):
        return self.t

    def getDeltaT(self):
        return self.deltaT
    
    def getStartT(self):
        return self.startT

    def getEndT(self):
        return self.endT

    def inc(self):
        self.t = self.t + self.deltaT
        return self

    def isEnd(self):
        if (self.endT <= self.t):
            return True

        return False