from tracemalloc import start
import ode_euler
import batch
import ode_env
import ode_time
import ode_control_input
import observer
import error_dynamics
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

class TestODEBatch(batch.Batch):
  # def __init__
  def __init__(self, deltaT, staetT, endT, startX, startXDot, f, env, observerEnvX, envT, controlInput):
    # ODEOneDimEulerMethod:
    # def __init__(self, deltaT, startT, endT, startX, startXDot):
    # def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT):
    self.odeEngine = ode_euler.ODEOneDimEulerMethod(deltaT, staetT, endT, startX, startXDot, f, env, envT, ode_control_input.ControlInput())
    self.observerEngine = ode_euler.ODEOneDimEulerMethod(deltaT, start, endT, startX + 2.0, startXDot + 2.0, f, observerEnvX, envT, controlInput)
    # self.odeEngine = ode_euler.ODEOneDimEulerMethod(0.01, 0, 100, 0.1, 0.1)
    self.resultT = []
    self.resultXDot = []
    self.resultX = []

    self.observerResultXDot = []
    self.observerResultX = []
    self.envT = envT


  def solve(self):
    # self.resultT, self.resultX, self.resultXDot = self.odeEngine.solve(f)

    # debug
    # implement odeEngine.inc() and use loop for several ode engine paralelly.
    for t in self.envT.startClock():
    # for result in self.odeEngine.solve(f, env, envT):
      # self.odeEngine.solve(f, env, envT)
      result = self.odeEngine.inc()
      resultObserver = self.observerEngine.inc()
      self.resultT.append(result[0])
      self.resultX.append(result[1])
      self.resultXDot.append(result[2])

      self.observerResultX.append(resultObserver[1])
      self.observerResultXDot.append(resultObserver[2])
    # end of debug

  def saveToFile(self):
    i = 0
    for t in self.resultT:
      x = self.resultX[i]
      xDot = self.resultXDot[i]
      output = "{0},{1},{2}".format(t, xDot, x)

      i = i + 1

    # プロット
    # plt.plot(self.resultT, self.resultX, label="test")
    plt.plot(self.resultXDot, self.resultX, label="actual system")
    plt.plot(self.observerResultXDot, self.observerResultX, label="observer")

    # 凡例の表示
    plt.legend()

    # プロット表示(設定の反映)
    plt.show()
    

# ddx = f(t, x, xDot)
f = lambda t, x, xDot: -1.0 * x - 0.5 * xDot
# f = lambda t, x, xDot: -1.0 * x - 0.5 * xDot - 2.0 * xDot**3
# f = lambda t, x, xDot: - 6.0 * x - 5.0 * xDot - 10.0 * t * x
# f = lambda t, x, xDot: - (6.0 + math.sin(t)) * x - (5.0 + math.cos(t)) * xDot - (2.0 * math.sin(t)) * x
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot + 3.0 * np.cos(x)
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot
# return (resultT, resultX, resultXDot)
env = ode_env.ODEEnv()
envObserver = ode_env.ODEEnv()
envT = ode_time.ODETime(0, 10.0, 0.01)

controlInput = ode_control_input.ControlInput()
controlInput.setEnvT(envT)
controlInput.setCoef([10, 10])

# def __init__(self, xEnv1, xEnv2):
errorDynamics = error_dynamics.ErrorDynamics(env, envObserver)
controlInput.setState(errorDynamics)

# def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT):
ode = TestODEBatch(0.01, 0, 100.0, 10.0, 5.0, f, env, envObserver, envT, controlInput)
ode.solve()
ode.saveToFile()