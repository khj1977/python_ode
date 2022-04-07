class ODEOneDimEulerMethod:
  def __init__(self, deltaT, startT, endT, startX, startXDot):
    self.deltaT = deltaT
    self.startT = startT
    self.endT = endT
    self.startX = startX
    self.startXDot = startXDot

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
      ddx = f(t, x, xDot)
      xDot = xDot + ddx * self.deltaT
      x = x + xDot * self.deltaT
      resultT.append(t)
      resultXDot.append(xDot)
      resultX.append(x)
      t = t + self.deltaT
      # print(x)

    return resultT, resultX, resultXDot