class ODETime:
    def __init__(self):
        self.t = 0

    def setT(self, t):
        self.t = t
        return self

    def getT(self):
        return self.t