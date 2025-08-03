from typing import Callable
from phoenix6.hardware import TalonFX
from phoenix6.configs import TalonFXConfiguration
from library.FaultLogger import FaultLogger
from library.TalonUtils import TalonUtils

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/lib/SimpleMotor.java
'''

class SimpleMotor:
    '''
    Simple Motor that utilizes a two callables for setting power and provides no feedback.
    Can work with TalonFXs and SparkBases. Can be closed with the specified Runnable.
    '''
    def __init__(self, setPower:Callable[[float], None], close:Callable[[], None]) -> None:
        '''
        Constructor.
        - `setPower` Callable for setting motor power.
        - `close` Callable for closing the motor.
        '''
        self._setPower = setPower
        self._close = close

    @staticmethod
    def talon(motor:TalonFX, config:TalonFXConfiguration) -> "SimpleMotor":
        '''
        - `RETURNS` a new SimpleMotor that controls a TalonFX motor. The motor is
          registered with TalonUtils and FaultLogger.
        - `motor` TalonFX controller instance with device ID.
        - `config` TalonFXConfiguration to apply to the motor.
        '''
        # TODO finish faultlogger
        # FaultLogger.registerTalon(motor)
        TalonUtils.addMotor(motor)
        motor.configurator.apply(config)
        return SimpleMotor(motor.set, motor.close)
    
    @staticmethod
    def none() -> "SimpleMotor":
        '''Returns a new SimpleMotor that does absolutely nothing.'''
        return SimpleMotor(lambda v: None, lambda: None)

    def setPower(self, power:float) -> None:
        '''Passes power into the callable specified in the constructor.'''
        self._setPower(power)
    
    def close(self) -> None:
        self._close()