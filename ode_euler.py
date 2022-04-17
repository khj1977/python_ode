class ODEOneDimEulerMethod:
  def __init__(self, deltaT, startT, endT, startX, startXDot):
    self.deltaT = deltaT
    self.startT = startT
    self.endT = endT
    self.startX = startX
    self.startXDot = startXDot

  def getDeltaT(self):
    return self.deltaT

  def getStartT(self):
    return self.startT

  def getEndT(self):
    return self.endT

  def getStartX(self):
    return self.startT

  def startXDot(self):
    return self.startXDot

  # f is function object
  def solve(self, f):
    x = self.startX
    xDot = self.startXDot
    resultT = []
    resultX = []
    resultXDot = []
    # for t in range(self.startT, self.endT, self.deltaT):
    t = self.startT
    while True:
      if t > self.endT:
        break

      # ODE
      # Hack the following to use multiple number of f()s to handle observer.
      ddx = f(t, x, xDot)
      # end of ODE

      xDot = xDot + ddx * self.deltaT
      x = x + xDot * self.deltaT

      yield [t, ddx, xDot, x]

      # debug
      # omit the following?
      resultT.append(t)
      resultXDot.append(xDot)
      resultX.append(x)
      # end of debug

      t = t + self.deltaT
      # print(x)

    return self
    # return resultT, resultX, resultXDot