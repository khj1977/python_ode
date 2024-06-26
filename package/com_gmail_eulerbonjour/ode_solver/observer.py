# from operator import truediv

# observer
class Observer:
  def __init__(self, odeEngineReal, odeEngineObserver, controlInput):
    self.odeEngineReal = odeEngineReal
    self.odeEngineObserver = odeEngineObserver

    self.controlInput = controlInput

    self.bresultT = []
    self.bresultX = []
    self.bresultXDot = []

  def inc(self):
    self.calcControlInput()
    self.applyControlInput(self.controlInput)
    result = self.xinc()

    return result

  def xinc(self):
    # debug
    # control input to applied to observer
    # odeEngineRelal is inc()ed by another method or scope.
    result = self.odeEngineObserver.inc()
    # end of debug

    return result

  def getControlInput(self):
    return self.controlInput

  # debug
  # implement the following method
  def calcControlInput(self):
    # return self
    self.controlInput.getStates().calcErr()
    self.controlInput.getStates().calcErrDot()
    self.controlInput.calcControlInput()
  # end of debug

  # debug
  # implement the following method
  # this may not br required since control is set to ode engine.
  def applyControlInput(self, controlInput):
    return self
  # end of debug

  # debug
  # this method is obsolete
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
  # end of debug
