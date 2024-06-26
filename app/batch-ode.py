from pickle import FALSE
from tracemalloc import start
from com_gmail_eulerbonjour.ode_solver.k_disturbance_observer import KDisturbanceObserver
from com_gmail_eulerbonjour.ode_solver.ode_coefs import ODECoefs
from com_gmail_eulerbonjour.ode_solver import ode_euler
from com_gmail_eulerbonjour.ode_solver import batch
from com_gmail_eulerbonjour.ode_solver import ode_env
from com_gmail_eulerbonjour.ode_solver import ode_time
from com_gmail_eulerbonjour.ode_solver import ode_control_input
from com_gmail_eulerbonjour.ode_solver import ode_robust_control_input
from com_gmail_eulerbonjour.ode_solver import ode_disturbance
from com_gmail_eulerbonjour.ode_solver import observer
from com_gmail_eulerbonjour.ode_solver import error_dynamics
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.fft import fft, ifft

class ODEBatch(batch.Batch):
  # def __init__
  def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, observerEnvX, envT, delta, rateLambda, controlInput, disturbance, initLambdas, nominalCoefs, kappa):
    # ODEOneDimEulerMethod:
    # def __init__(self, deltaT, startT, endT, startX, startXDot):
    # def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT):
    # self.odeEngine = ode_euler.ODEOneDimEulerMethod(deltaT, staetT, endT, startX, startXDot, f, env, envT, ode_control_input.ControlInput(), disturbance)

    # debug
    # refactor ODE engine to handle two control inputs for cancel out disturbance and 
    # control of nominal system
    ## controlInputReal = ode_control_input.ControlInput()
    controlInputReal = ode_robust_control_input.RobustControlInput()
    controlInputNominalReal = ode_control_input.ControlInput()

    # debug
    # call some methods for controlInputNominalReal for control of 
    # unstable nominal system.
    # end of debug

    # def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT, controlInput, controlInputNominal, disturbance):
    self.odeEngine = ode_euler.ODEOneDimEulerMethod(deltaT, startT, endT, startX, startXDot, f, env, envT, controlInputReal, controlInputNominalReal, disturbance)
    self.disturbance = disturbance
    # end of debug

    disturbanceF = lambda t, x, xDot: 0.0
    self.observerEngine = ode_euler.ODEOneDimEulerMethod(deltaT, start, endT, startX + 2.0, startXDot + 2.0, f, observerEnvX, envT, controlInput, controlInputNominalReal,ode_disturbance.Disturbance(disturbanceF, env, envT))
    # self.odeEngine = ode_euler.ODEOneDimEulerMethod(0.01, 0, 100, 0.1, 0.1)
    # def __init__(self, odeEngineReal, odeEngineObserver, controlInput):
    self.observer = observer.Observer(self.odeEngine, self.observerEngine, controlInput)
    # self.controlInput = controlInput

    # debug
    # The last argument may be changed.
    # def __init__(self, odeEngineReal, controlInputReal, envT, f, startX, startXDot):

     # def __init__(self, odeEngineReal, controlInputReal, controlInputNominalReal, envT, f, startX, startXDot, delta, rateLambda, initLambdas, nominalCoefs, kappa)
    self.disturbanceObserver = KDisturbanceObserver(self.odeEngine, controlInputReal, controlInputNominalReal, envT, f, startX, startXDot, delta, rateLambda, initLambdas, nominalCoefs, kappa)
    # end of debug

    estimatedDisturbance = self.disturbanceObserver.getEstimatedDisturbanceDynamics()
    controlInputReal.setDisturbance(estimatedDisturbance)

    self.resultT = []

    self.resultXDot = []
    self.resultX = []

    self.observerResultXDot = []
    self.observerResultX = []

    self.disturbanceObserverResultX = []
    self.disturbanceObserverResultXDot = []

    self.modifiedReferemceResultX = []

    self.ffResultX = []

    self.envT = envT

    self.errorResultXDot = []
    self.errorResultX = []

    self.controlResultXDot = []
    self.controlResultX = []

    self.disturbanceResultXDot = []
    self.disturbanceResultX = []

    self.estimationError = []

    self.resultLambda = []

  def solve(self):
    # self.resultT, self.resultX, self.resultXDot = self.odeEngine.solve(f)

    # debug
    # implement odeEngine.inc() and use loop for several ode engine paralelly.
    # errorDynamics = self.observerEngine.getControlInput().getStates()
    errorDynamics = self.disturbanceObserver.getErrorDynamics()
    modifiedSignal = self.disturbanceObserver.getModifiedReference()
    ff = self.disturbanceObserver.getFFSignal()
    for t in self.envT.startClock():
    # for result in self.odeEngine.solve(f, env, envT):
      # self.odeEngine.solve(f, env, envT)
      result = self.odeEngine.inc()
      # resultObserver = self.observerEngine.inc()
      # resultObserver = self.observer.inc()
      resultKDO = self.disturbanceObserver.inc()

      # debug
      # self.disturbance.calcDynamics()
      # end of debug
      # debug
      # The following is really required?
      self.disturbance.calcDisturbanceDot()
      # end of debug

      self.resultT.append(result[0])
      self.resultX.append(result[1])
      self.resultXDot.append(result[2])

      # self.observerResultX.append(resultObserver[1])
      # self.observerResultXDot.append(resultObserver[2])

      self.disturbanceObserverResultX.append(resultKDO[1])
      self.disturbanceObserverResultXDot.append(resultKDO[2])

      # debug
      # print(resultKDO[1])
      # end of debug

      self.modifiedReferemceResultX.append(modifiedSignal.getX())
      self.ffResultX.append(ff.getX())

      # debug
      # is it really getX1()? There may be a bug
      self.errorResultX.append(errorDynamics.getX())
      self.errorResultXDot.append(errorDynamics.getX2())
      # end of debug

      self.controlResultX.append(-1.0 * self.disturbanceObserver.getEstimatedDisturbanceDynamics().getControlInput())
      self.controlResultXDot.append(-1.0 * self.disturbanceObserver.getEstimatedDisturbanceDynamics().getControlInputDot())

      # add disturbance array to obtain dynamics of disturbance to list
      disturbanceVals = self.disturbance.getStates()
      self.disturbanceResultX.append(disturbanceVals[1])
      self.disturbanceResultXDot.append(disturbanceVals[2])

      # debug
      # it should be norm?
      estimationError = -1.0 * self.disturbanceObserver.getEstimatedDisturbanceDynamics().getControlInput() - disturbanceVals[1]
      # print(estimationError)
      self.estimationError.append(estimationError)
      # end of debug
    # end of debug

  def saveToFileTime(self, tMax, xMin, xMax):
    plt.ylim(xMin, xMax)
    plt.xlim(0, tMax)
    plt.plot(self.resultT, self.resultX, label="actual system")
    # plt.plot(self.resultT, self.disturbanceObserverResultX, label="disturbance observer")
    # plt.plot(self.resultT, self.controlResultX, label="estimated disturbance")
    # plt.plot(self.resultT, self.disturbanceResultX, label="disturbance")
    # plt.plot(self.resultT, self.disturbanceObserver.getResultLambdas(), label="lambda")
    #plt.plot(self.resultT, self.modifiedReferemceResultX, label="modified signal")
    #plt.plot(self.resultT, self.ffResultX, label="ff signal")
    # plt.plot(self.resultT, self.errorResultX, label="error")
    # plt.plot(self.resultT, self.estimationError, label="estimation error")

    # 凡例の表示
    plt.legend()

    # プロット表示(設定の反映)
    plt.show()

  def saveToFile(self, xMin, xMax, yMin, yMax):
    i = 0
    for t in self.resultT:
      x = self.resultX[i]
      xDot = self.resultXDot[i]
      output = "{0},{1},{2}".format(t, xDot, x)

      i = i + 1

    # プロット
    # debug
    plt.xlim(xMin, xMax)
    plt.ylim(yMin, yMax)
    # end of debug

    # plt.plot(self.resultT, self.resultX, label="test")

    plt.plot(self.resultXDot, self.resultX, label="actual system")
    # plt.plot(self.observerResultXDot, self.observerResultX, label="observer")
    # plt.plot(self.errorResultXDot, self.errorResultX, label="error")
    # plt.plot(self.controlResultXDot, self.controlResultX, label="estimated disturbance")
    
    plt.plot(self.disturbanceResultXDot, self.disturbanceResultX, label="disturbance")
    # plt.plot(self.disturbanceObserverResultXDot, self.disturbanceObserverResultX, label="disturbance observer")
    # 凡例の表示
    plt.legend()

    # プロット表示(設定の反映)
    plt.show()
    

# ddx = f(t, x, xDot)
# f = lambda t, x, xDot: -1.0 * x - 0.5 * xDot
# f = lambda t, x, xDot: -1.0 * x - 5.0 * xDot - 2.0 * xDot**3
# f = lambda t, x, xDot: -6.0 * x - 5.0 * xDot - 1.0 * xDot**3
# f = lambda t, x, xDot: - 6.0 * x - 5.0 * xDot - 10.0 * t * x
# f = lambda t, x, xDot: - (6.0 + math.sin(t)) * x - (5.0 + math.cos(t)) * xDot - (2.0 * math.sin(t)) * x
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot + 3.0 * np.cos(x)
# nominal for void disturbance
# f = lambda t, x, xDot: -2.0 * x - 1.0 * xDot

# eig value is [1] 1+1.414214i 1-1.414214i
# f = lambda t, x, xDot: -3.0 * x + 2.0 * xDot

# > I = matrix(c(0, -0.02, 1, -0.3), nrow=2)
# > eigen(I)
# eigen() decomposition
# $values
# [1] -0.2 -0.1
# 
# $vectors
#            [,1]        [,2]
# [1,] -0.9805807  0.99503719
# [2,]  0.1961161 -0.09950372
# 
# > I
#       [,1] [,2]
# [1,]  0.00  1.0
# [2,] -0.02 -0.3

# f = lambda t, x, xDot: -0.02 * x - 0.3 * xDot
# f = lambda t, x, xDot: -0.02 * x - 0.03 * xDot
# f = lambda t, x, xDot: -0.02 * x

# The following diff eq has been derived by the first prototype of digital
# lagrangian for nonlinear smart material systems for most simple case.
# Since it is the most simple case, it does not deploy correlation between
# theta_i and theta_i+1, etc. It is based on night napkin based work,
# there could be mistake. It would be investigated seriously later one.
# f = lambda t, x, xDot: -1.2 * math.cos(x) - 0.1 * x * xDot
f = lambda t, x, xDot: -1.2 * math.cos(x)
# f = lambda t, x, xDot: -0.3 * xDot

# f = lambda t, x, xDot: -6.0 * x - 5.0 * xDot
# f = lambda t, x, xDot: 1.0 * x + 6.0 * xDot
# init lambdas are eigen vals of nominal system.
initLambdas = [-5.0, -4.9]
# nominal for void disturbance
# nominalCoefs = [-2.0, -1.0]
# nominalCoefs = [6.0, 10.0]
nominalCoefs = [-0.02, 0.00]
# f = lambda t, x, xDot: -3.0 * x - 0.1 * math.sin(2.0 * x) * x * xDot
# f = lambda t, x, xDot: -3.0 * x - 0.1 * xDot
# f = lambda t, x, xDot: -6.0 * x - 5.0 * xDot
# f = lambda t, x, xDot: -3.0 * x - 0.001 * xDot
# f = lambda t, x, xDot: -3.0 * x
# f = lambda t, x, xDot: -3.0 * x - 0.1 * x * xDot
# f = lambda t, x, xDot: -3.0 * x - 0.4 * math.sin(x) * x * xDot
# f = lambda t, x, xDot: -3.0 * x - 2.0 * math.sin(1.0 * x) * x * xDot
# return (resultT, resultX, resultXDot)
env = ode_env.ODEEnv()
envObserver = ode_env.ODEEnv()
endT = 100.0
envT = ode_time.ODETime(0, endT, 0.01)

controlInput = ode_control_input.ControlInput()
controlInput.setEnvT(envT)
coefs = ODECoefs()
# coefs.setCoefs([3.0, 15.0])
coefs.setCoefs([0.0, 0.0])
# coefs.setCoefs([10.0, 15.0])
# coefs.setCoefs([6.0, 5.0])
controlInput.setCoef(coefs)

# debug
# define eq which is first arg.
# f = lambda t, x, xDot: - (6.0 + math.sin(t)) * x - (5.0 + math.cos(t)) * xDot - (2.0 * math.sin(t)) * x
# disturbanceF = lambda t, x, xDot: -2.0 * x - 1.0 * xDot
# disturbanceF = lambda t, x, xDot: -1.0 * math.sin(t) * x - math.cos(t) * xDot - 2.0 * math.sin(t) * x + 4.0 * math.sin(t)

# nonlinear void disturbance
# disturbanceF = lambda t, x, xDot: -1.0 * math.sin(t) * x - math.cos(t) * xDot - 2.0 * math.sin(t) * x + 6.0 * math.sin(t)

# unstable controller
# disturbanceF = lambda t, x, xDot: -12.0 * x - 15.0 * xDot

# periodical controller
# disturbanceF = lambda t, x, xDot: -3.0 * x + -7.0 * xDot

# disturbanceF = lambda t, x, xDot: -0.3 * xDot
# disturbanceF = lambda t, x, xDot: 0.0
# disturbanceF = lambda t, x, xDot: -0.0001 * x*x*x
disturbanceF = lambda t, x, xDot: 0.0
# disturbanceF = lambda t, x, xDot: -1.5 * xDot 

# disturbanceF = lambda t, x, xDot: 2.0 * math.sin(1.0 * t)
# disturbanceF = lambda t, x, xDot: 0.5 * math.sin(1.0 * t)
# disturbanceF = lambda t, x, xDot: -1.0 * x*x*x + 0.5 * math.sin(1.0 * t)
# disturbanceF = lambda t, x, xDot: 0.5 * math.sin(1.0 * t) + 0.2 * math.sin(2.0 * t)
# disturbanceF = lambda t, x, xDot: 0.0

# disturbanceF = lambda t, x, xDot: 0.0
# disturbanceF = lambda t, x, xDot: 1.0 * x - 1.5 * xDot
# disturbanceF = lambda t, x, xDot: 4.0 * x + 1.5 * xDot
# disturbanceF = lambda t, x, xDot: 1.0 * math.sin(t)
disturbance = ode_disturbance.Disturbance(disturbanceF, env, envT)
# end of debug

# def __init__(self, xEnv1, xEnv2):
errorDynamics = error_dynamics.ErrorDynamics(env, envObserver, envT, FALSE)
controlInput.setState(errorDynamics)

# def __init__(self, deltaT, startT, endT, startX, startXDot, f, env, envT):
# def __init__(self, deltaT, staetT, endT, startX, startXDot, f, env, observerEnvX, envT, controlInput, disturbance):
env.setX(10.0)
env.setXDot(5.0)
# def __init__(self, deltaT, staetT, endT, startX, startXDot, f, env, observerEnvX, envT, delta, rateLambda, controlInput, disturbance, initLambdas, nominalCoefs, kappa):
delta = 0.00001
odeBatch = ODEBatch(0.01, 0, 10.0, 10.0, 5.0, f, env, envObserver, envT, delta, 0.01, controlInput, disturbance, initLambdas, nominalCoefs, 0.2)
odeBatch.solve()

# plot
# odeBatch.saveToFile(-200.0, 200.0, -200.0, 200.0)
# odeBatch.saveToFile(4.0, 6.0, -2.0, 2.0)
# odeBatch.saveToFile(-0.05, 0.05, -0.05, 0.05)
# odeBatch.saveToFile(-3.0, 3.0, -3.0, 3.0)
# ode.saveToFile(-0.05, 0.05, -0.05, 0.05)
# odeBatch.saveToFile(-10.0, 10.0, -10.0, 10.0)

# odeBatch.saveToFileTime(100.0, -100.0, 100.0)
odeBatch.saveToFileTime(endT, -5.0, 5.0)
# odeBatch.saveToFileTime(endT, -1200.0, 1020.0)
# odeBatch.saveToFileTime(100.0, -40.0, 40.0)
# odeBatch.saveToFileTime(100.0, -4.5, 4.5)