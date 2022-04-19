class ControlInput:
    def __init__(self):
        self.u = 0.0
        # return self
    
    def getControlInput(self):
        return self.u

    def getState(self):
        return self.env

    def setState(self, env):
        self.env = env

        return self

    def setControlInput(self, controlInput):
        self.u = ControlInput

        return self

    def calcControlInput(self):
        # debug
        # implement this method
        return self
        # end of debug
 
