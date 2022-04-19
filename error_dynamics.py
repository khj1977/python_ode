from tkinter import E


class ErrorDynamics:

    def __init__(self, xEnv1, xEnv2):
        self.x1 = xEnv1
        self.x2 = xEnv2   
        self.calcErr()
        
    def calcErr(self):
        x1 = self.x1.getX()
        x2 = self.x2.getX()

        self.err = x1 - x2

        return self

    def get2Norm(self):
        self.calcErr()
        e = self.err
        norm = e * e

        return norm