from posixpath import supports_unicode_filenames
from error_dynamics import ErrorDynamics
from ode_control_input import ControlInput
from ode_disturbance import Disturbance
from ode_env import ODEEnv
import ode_euler
import ode_coefs
import ode_control_input
import math

class KDisturbanceObserver:
    def __init__(self, odeEngineReal, controlInputReal, envT, f, startX, startXDot):
        self.odeEngineReal = odeEngineReal
        self.envT = envT
        self.states = ODEEnv()
        self.f = f
        self.controlInputReal = controlInputReal
        # self.controlInput = controlInput
        # control input for observer not actual system or modified refernece signal.
        self.controlInput = ControlInput()

        # def __init__(self, eq, envX, envT):
        disturbanceF = lambda t, x, xDot: 0.0
        nullDisturbance = Disturbance(disturbanceF, self.states, self.envT)
        self.odeEngineFF = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, ODEEnv(), self.envT, controlInputReal, nullDisturbance)
        
        #  def __init__(self, xEnv1, xEnv2, envT):
        # r_bDot = Ar_b + Bp
        self.modifiedSignalDynamics = ErrorDynamics(self.odeEngineReal.getStates(), self.odeEngineFF.getStates(), self.envT)
        
        # disturbance observer follows modified reference signal.
        # u = K(t) * e(t) where e(t)  = x - r_b where r_b = self.modifiedSignalDynamics
        # errorDynamics = error_dynamics.ErrorDynamics(env, envObserver, envT)
        # controlInput.setState(errorDynamics)

        # self.f = lambda x, t, z: 0.0

        # debug
        # really self.states?
        # end of debug
        self.disturbanceObserverEngine = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, self.states, envT, self.controlInput, nullDisturbance)

        self.errorDynamics = ErrorDynamics(self.disturbanceObserverEngine.getStates(),  self.modifiedSignalDynamics, self.envT)

        coefs = ode_coefs.ODECoefs()
        coefs.setCoefs([-3.0, -15.0])
        # coefs.setCoefs([10.0, 15.0])
        # coefs.setCoefs([6.0, 5.0])
        self.controlInput.setCoef(coefs)
        self.controlInput.setEnvT(self.envT)
        self.controlInput.setState(self.errorDynamics)


    def inc(self):
        self.calcControlInput()
        self.applyControlInput(self.controlInput)
        result = self.xinc()

        self.controlInputReal.setControlInput(-1.0 * self.controlInput.getControlInput())

        # debug
        # print(self.odeEngineFF.getStates().getX())
        # print(self.modifiedSignalDynamics.getX())
        # print(self.states.getX())
        # print(self.errorDynamics.getX())
        # end of debug

        return result

    def xinc(self):
        # debug
        # control input to applied to observer
        # odeEngineRelal is inc()ed by another method or scope.
        self.odeEngineFF.inc()
        result = self.disturbanceObserverEngine.inc()
        # end of debug

        return result

    def getEstimatedDisturbanceDynamics(self):
        return self.controlInput

    # debug
    # implement the following method
    def calcControlInput(self):
        # debug
        # make this algo adaptive.
        # end of debug

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