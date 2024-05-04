class ODECoefs:
    def __init__(self):
        pass

    def setCoefs(self, coefsList):
        self.coef = coefsList

    def yieldCoefs(self):
        for a in self.coef:
            yield a

        # return self