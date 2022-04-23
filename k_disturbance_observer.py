from posixpath import supports_unicode_filenames
from error_dynamics import ErrorDynamics
from ode_control_input import ControlInput
from ode_env import ODEEnv
import ode_euler
import ode_control_input

class KDisturbanceObserver:
    def __init__(self, odeEngineReal, envT, f, startX, startXDot):
        self.odeEngineReal = odeEngineReal
        self.envT = envT
        self.states = ODEEnv()
        self.f = f
        self.controlInput = ControlInput()
        self.odeEngineFF = ode_euler.ODEOneDimEulerMethod(envT.getDeltaT(), envT.getStartT(), envT.getEndT(), startX, startXDot, self.f, self.states, self.nvT, ode_control_input.ControlInput())
        #  def __init__(self, xEnv1, xEnv2, envT):
        self.modifiedSignalDynamics = ErrorDynamics(self.odeEngineReal.getStates(), self.odeEngineFF.getStates(), self.envT)

    def inc(self):
        # debug
        # implement the following
        return self
        # end of debug