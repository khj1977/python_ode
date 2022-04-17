class ODEEnv:
    def __init__(self):
        self.x = 0.0
        self.xddot = 0.0
        self.xdot = 0.0
        self.t = 0.0
    
    def setX(self, x):
        self.x = x
        return self
    
    def setXDot(self, xdot):
        self.xdot = xdot
        return self

    def setXDDot(self, xddot):
        self.xddot = xddot
        return self

    def setT(self, t):
        self.t = t
        return self

    def getX(self):
        return self.x

    def getXDot(self):
        return self.xdot

    def getXDDot(self):
        return self.xddot

    def getT(self):
        return self.t