import ode_euler
import batch
import ode_env
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

class TestODEBatch(batch.Batch):
  # def __init__
  def __init__(self):
    # ODEOneDimEulerMethod:
    # def __init__(self, deltaT, startT, endT, startX, startXDot):
    self.odeEngine = ode_euler.ODEOneDimEulerMethod(0.01, 0, 100.0, 0.05, 0.05)
    # self.odeEngine = ode_euler.ODEOneDimEulerMethod(0.01, 0, 100, 0.1, 0.1)
    self.resultT = []
    self.resultXDot = []
    self.resultX = []


  def solve(self, f, env):
    # self.resultT, self.resultX, self.resultXDot = self.odeEngine.solve(f)
    for result in self.odeEngine.solve(f, env):
      self.resultT.append(result[0])
      self.resultX.append(result[1])
      self.resultXDot.append(result[2])

  def saveToFile(self):
    i = 0
    for t in self.resultT:
      x = self.resultX[i]
      xDot = self.resultXDot[i]
      output = "{0},{1},{2}".format(t, xDot, x)

      i = i + 1

    # プロット
    # plt.plot(self.resultT, self.resultX, label="test")
    plt.plot(self.resultXDot, self.resultX, label="test")

    # 凡例の表示
    plt.legend()

    # プロット表示(設定の反映)
    plt.show()
    

# ddx = f(t, x, xDot)
# f = lambda t, x, xDot: -1.0 * x - 0.5 * xDot
# f = lambda t, x, xDot: -1.0 * x - 0.5 * xDot - 2.0 * xDot**3
# f = lambda t, x, xDot: - 6.0 * x - 5.0 * xDot - 10.0 * t * x
f = lambda t, x, xDot: - (6.0 + math.sin(t)) * x - (5.0 + math.cos(t)) * xDot - (2.0 * math.sin(t)) * x
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot + 3.0 * np.cos(x)
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot
# return (resultT, resultX, resultXDot)
env = ode_env.ODEEnv()
ode = TestODEBatch()
ode.solve(f, env)
ode.saveToFile()