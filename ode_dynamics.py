class Dynamics:

    def __init__(self, odeEngine, envT):
        self.odeEngine = odeEngine
        self.envT = envT
        self.prevX = False

    def getX(self):
        return self.odeEngine.getStates().getX()

    def getXDot(self):
        return self.odeEngine.getStates().getXDot()