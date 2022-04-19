from operator import truediv


class Observer:
  def __init__(self, odeEngineReal, odeEngineObserver):
    self.odeEngineReal = odeEngineReal
    self.odeEngineObserver = odeEngineObserver

    self.bresultT = []
    self.bresultX = []
    self.bresultXDot = []

  def inc(self):
    controlInput = self.calcControlInput()
    self.applyControlInput(controlInput)
    self.xinc()

    return self

  def xinc(self):
    self.odeEngineObserver.inc()

    return self

  def calcControlInput(self):
    return self

  def applyControlInput(self):
    return self

  def solve(self):
    t = 0.0
    e = be0
    while t > self.endT:
      nominalData = self.odeEngineReal.solve(self.orgODE)
      observerData = self.odeEngineObserver.solve(
        self.orgODEObserver, 
        self.orgControlObserver
        )

      # feedforward observer and data for K-DO.
      # errorData = nominalData - observerData (and feedforward for K-DO) 
      # control input = K(t) * error
      # yield estimated uncertainty.
