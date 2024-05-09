from com_gmail_eulerbonjour.ode_solver import ode_euler as euler

class ProgrammableInput:

    def __init__(self, odeEngine):
        self.engine = odeEngine
        self.val = 0.0

    def setNumericInput(self, aValue):
        self.val = aValue

        return self
    
    def getNumericInput(self):
        return self.val
    
    def getControlInput(self):
        return self.getNumericInput()