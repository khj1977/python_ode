import ode_env

class ODEOneDimEulerMethod:
  def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT, controlInput, disturbance):
    self.env = env
    self.envT = envT

    self.deltaT = deltaT
    self.startT = startT
    self.endT = endT
    self.startX = startX
    self.startXDot = startXDot

    self.env.setX(startX)
    self.env.setXDot(startXDot)

    self.diffEQ = f
    self.env = env
    self.envT = envT

    self.controlInput = controlInput
    self.disturbance = disturbance

    self.resultT = []
    self.resultX = []
    self.resultXDot = []

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

  def getControlInput(self):
    return self.controlInput

  def getStates(self):
    return self.env

  def inc(self):
    # debug
    # return [t, ddx, xDot, x]
    # end of debug
    # x = self.startX
    # xDot = self.startXDot
    x = self.env.getX()
    xDot = self.env.getXDot()

    # debug
    # for t in range(self.startT, self.endT, self.deltaT):
    # end of debug
    # t = self.startT
    t = self.envT.getT()
    deltaT = self.envT.getDeltaT()

    # if t > self.endT:
    # if not self.envT.isEnd():
    #   return False

    # ODE
    # Hack the following to use multiple number of f()s to handle observer.
    # make t, x, xdot env to enclose to handle multple phase env namely: PhaseEnv
    # ddx = self.diffEQ(t, x, xDot) + self.controlInput.getControlInput() + self.disturbance.calcDynamics()
    ddx = self.diffEQ(t, x, xDot) 
    ddx = ddx + self.controlInput.getControlInput() + self.disturbance.calcDynamics()
    # ddx = self.diffEQ(t, x, xDot)
    # end of ODE

    # xDot = xDot + ddx * self.deltaT
    xDot = xDot + ddx * deltaT
    x = x + xDot * self.deltaT

    self.env.setX(x)
    self.env.setXDot(xDot)
    self.env.setXDDot(ddx)
    # self.env.setT(t)

    # debug
    # omit the following?
    self.resultT.append(t)
    self.resultXDot.append(xDot)
    self.resultX.append(x)
    # end of debug

    # t = t + self.deltaT
    # print(x)

    return [t, ddx, xDot, x]

  # f is function object
  def solve(self, f, env, envT):
    x = self.startX
    xDot = self.startXDot
    resultT = []
    resultX = []
    resultXDot = []
    # debug
    # for t in range(self.startT, self.endT, self.deltaT):
    # end of debug
    # t = self.startT
    t = envT.getStartT()
    deltaT = envT.getDeltaT()
    while True:
      # if t > self.endT:
      if not envT.isEnd():
        break

      # ODE
      # Hack the following to use multiple number of f()s to handle observer.
      # make t, x, xdot env to enclose to handle multple phase env namely: PhaseEnv
      ddx = f(t, x, xDot)
      # end of ODE

      # xDot = xDot + ddx * self.deltaT
      xDot = xDot + ddx * deltaT
      x = x + xDot * self.deltaT

      env.setX(x)
      env.setXDot(xDot)
      env.setXDDot(ddx)
      env.setT(t)

      yield [t, ddx, xDot, x]

      # debug
      # omit the following?
      resultT.append(t)
      resultXDot.append(xDot)
      resultX.append(x)
      # end of debug

      # t = t + self.deltaT
      envT.inc()
      t = envT.getT()
      # print(x)

    return self
    # return resultT, resultX, resultXDot