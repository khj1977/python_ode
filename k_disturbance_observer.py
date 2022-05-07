from posixpath import supports_unicode_filenames
from error_dynamics import ErrorDynamics
from ode_control_input import ControlInput
from ode_env import ODEEnv
import ode_euler
import ode_control_input

class KDisturbanceObserver:
    def __init__(self, odeEngineReal, controlInputReal, envT, f, startX, startXDot):
        self.odeEngineReal = odeEngineReal
        self.envT = envT
        self.states = ODEEnv()
        self.f = f
        # self.controlInput = controlInput
        # control input for observer not actual system or modified refernece signal.
        self.controlInput = ControlInput()

        self.odeEngineFF = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, self.states, self.envT, controlInputReal)
        
        #  def __init__(self, xEnv1, xEnv2, envT):
        # r_bDot = Ar_b + Bp
        self.modifiedSignalDynamics = ErrorDynamics(self.odeEngineReal.getStates(), self.odeEngineFF.getStates(), self.envT)
        
        # disturbance observer follows modified reference signal.
        # u = K(t) * e(t) where e(t)  = x - r_b where r_b = self.modifiedSignalDynamics
        # errorDynamics = error_dynamics.ErrorDynamics(env, envObserver, envT)
        # controlInput.setState(errorDynamics)
        self.controlInput.setState(self.modifiedSignalDynamics)

        self.disturbanceObserverEngine = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, self.states, envT, self.controlInput)

        self.errorDynamics = ErrorDynamics(self.modifiedSignalDynamics, self.disturbanceObserverEngine.getStates(), self.envT)

        self.controlInput.setState(self.errorDynamics)


    def inc(self):
        self.calcControlInput()
        self.applyControlInput(self.controlInput)
        result = self.xinc()

        return result

    def xinc(self):
        # debug
        # control input to applied to observer
        # odeEngineRelal is inc()ed by another method or scope.
        result = self.disturbanceObserverEngine.inc()
        # end of debug

        return result

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