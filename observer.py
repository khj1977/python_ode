class Observer:
  def __init__(self, odeEngin, f, bx0, bxDot0, be0):
    self.odeEngine = odeEngine
    self.orgODE = f
    self.bx0 = x0
    self.bxDot0 = xDot0
    self.e0 = e0
    self.bresultT = []
    self.bresultX = []
    self.bresultXDot = []

  def solve(self):