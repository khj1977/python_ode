from pickle import FALSE, TRUE
from posixpath import supports_unicode_filenames
from error_dynamics import ErrorDynamics
from ode_control_input import ControlInput
from ode_disturbance import Disturbance
from ode_env import ODEEnv
import ode_euler
import ode_coefs
import ode_control_input
import math
from numpy import linalg as la
import numpy as np

class KDisturbanceObserver:
    def __init__(self, odeEngineReal, controlInputReal, controlInputNominalReal, envT, f, startX, startXDot, delta, rateLambda, initLambdas, nominalCoefs, kappa):
        self.odeEngineReal = odeEngineReal
        self.envT = envT
        self.states = ODEEnv()
        self.f = f
        self.delta = delta
        self.rateLambda = rateLambda
        self.controlInputReal = controlInputReal
        self.controlInputNominalReal = controlInputNominalReal
        # self.controlInput = controlInput
        # control input for observer not actual system or modified refernece signal.
        self.controlInput = ControlInput()
        self.lambdas = initLambdas
        self.kappa = kappa
        self.nominalCoefs = nominalCoefs

        # debug
        # There may be bug around the following since the disturbance is not canceled 
        # out if estimated disturbance is feedbacked but twice of estimated disturbance.
        # def __init__(self, eq, envX, envT):
        disturbanceF = lambda t, x, xDot: 0.0
        nullDisturbance = Disturbance(disturbanceF, self.states, self.envT)
        self.odeEngineFF = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, ODEEnv(), self.envT, self.controlInputReal, ControlInput(), nullDisturbance)
        # end of debug
        
        #  def __init__(self, xEnv1, xEnv2, envT):
        # r_bDot = Ar_b + Bp
        # self.modifiedSignalDynamics = ErrorDynamics(self.odeEngineReal.getStates(), self.odeEngineFF.getStates(), self.envT)
        self.modifiedSignalDynamics = ErrorDynamics(self.odeEngineReal.getStates(), self.odeEngineFF.getStates(), self.envT, FALSE)
        
        # disturbance observer follows modified reference signal.
        # u = K(t) * e(t) where e(t)  = x - r_b where r_b = self.modifiedSignalDynamics
        # errorDynamics = error_dynamics.ErrorDynamics(env, envObserver, envT)
        # controlInput.setState(errorDynamics)

        # self.f = lambda x, t, z: 0.0

        # debug
        # really self.states?
        # end of debug

        # debug
        # the following def control may cause bug.
        # end of debug
        self.disturbanceObserverEngine = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, self.states, envT, self.controlInputNominalReal, self.controlInput, nullDisturbance)

        self.errorDynamics = ErrorDynamics(self.disturbanceObserverEngine.getStates(),  self.modifiedSignalDynamics, self.envT, FALSE)

        # debug
        # Controller for disturbance observer which is estimated disturbance
        coefs = ode_coefs.ODECoefs()
        coefs.setCoefs([1000.0, 3000.0])
        # coefs.setCoefs([10.0, 50.0])
        # coefs.setCoefs([6.0, 5.0])
        self.controlInput.setCoef(coefs)
        self.controlInput.setEnvT(self.envT)
        self.controlInput.setState(self.errorDynamics)
        # end of debug


    def inc(self):
        # debug
        # The following block could go to xinc().
        # print(self.errorDynamics.getErr())
        self.modifiedSignalDynamics.calcErr()
        self.errorDynamics.calcErr()
        # end of debug

        self.calcControlInput()
        self.applyControlInput(self.controlInput)
        result = self.xinc()

        # feedback estimated disturbance to actual system for closed loop system
        # self.controlInputReal.setControlInput(self.controlInput.getControlInput())

        return result

    def xinc(self):
        # debug
        # control input to applied to observer
        # odeEngineRelal is inc()ed by another method or scope.
        self.odeEngineFF.inc()
        result = self.disturbanceObserverEngine.inc()

        self.modifiedSignalDynamics.calcErrDot()
        self.errorDynamics.calcErrDot()
        # end of debug

        return result

    def getModifiedReference(self):
        return self.modifiedSignalDynamics

    def getEstimatedDisturbanceDynamics(self):
        return self.controlInput

    def getFFSignal(self):
        return self.odeEngineFF.getStates()

    def getErrorDynamics(self):
        return self.errorDynamics

    # debug
    # implement the following method
    def calcControlInput(self):
        # debug
        # make this algo adaptive.
        # end of debug
        lyapunovValue = self.errorDynamics.getTrans2Norm(self.lambdas)
        # debug
        # print(lyapunovValue)
        # end of debug
        if lyapunovValue < self.delta:
            lambdaDot = 0.0
        else:
            lambdaDot = self.rateLambda
            # lambdaDot = 0.01
        # debug
        # calc gain with lanbdaDot
        # self.kappa = 0.2

        # a21 = -6.0
        # a22 = -5.0
        # l1 = 10.0
        # l2 = 20.0
        # k1 = -1.0 * (l1 * l2) - a21
        # k2 = -1.0 * (l1 + l2) - a22
        # a = np.array([[0., 1.], [a21 + k1, a22 + k2]])
        # w, v = la.eig(a)
        # print(w)

        lambda1 = self.lambdas[0] + lambdaDot
        # lambda2 = lambda1 * self.kappa
        lambda2 = lambda1 * 0.2
        k1 = -1.0 * (lambda1 * lambda2) - self.nominalCoefs[0]
        k2 = -1.0 * (lambda1 + lambda2) - self.nominalCoefs[1]

        self.lambdas[0] = lambda1
        self.lambdas[1] = lambda2

        coef = self.controlInput.getCoef()
        gain = [k1, k2]
        # gain = [60.0, 50.0]
        coef.setCoefs(gain)

        # debug
        # a = np.array([[0., 1.], [self.nominalCoefs[0] + k1, self.nominalCoefs[1] + k2]])
        # w, v = la.eig(a)
        # print(gain)
        # print(w)
        # end of debug

        # self.controlInput.setCoef(coef)
        # end of debug

        # return self
        # self.controlInput.getStates().calcErr()
        # self.controlInput.getStates().calcErrDot()

        self.controlInput.calcControlInput()
        # end of debug

    # debug
    # implement the following method
    # this may not br required since control is set to ode engine.
    def applyControlInput(self, controlInput):
        return self
    # end of debug