from operator import truediv


class Observer:
  def __init__(self, odeEngineReal, f_ode, odeEngineObserver, f_observer, f_control_observer, bx0, bxDot0, be0):
    self.odeEngineReal = odeEngineReal
    self.odeEngineObserver = odeEngineObserver
    self.orgODE = f_ode
    self.orgDEObserver = f_observer
    self.orgControlObserver = f_control_observer
    self.bx0 = bx0
    self.bxDot0 = bxDot0
    self.e0 = be0
    self.bresultT = []
    self.bresultX = []
    self.bresultXDot = []

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
