from wpilib import DigitalInput
from typing import Callable
from LoggingUtils import Log

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/lib/FaultLogger.java
'''

class Beambreak:
    '''
    A beambreak wrapper that contains two main elements: 1. A callable that supplies a boolean
    detailing the beambreak's state; true for unbroken, false for broken. 2. A runnable that
    will close all resources as necessary.
    '''
    def __init__(self, beambreak:Callable[[], bool], close:Callable[[], None]) -> None:
        self._beambreak = beambreak
        self._close = close
    
    @staticmethod
    def real(channel:int) -> "Beambreak":
        '''
        Generates a beambreak wrapper based off a channel.
        - `channel` the channel for the beambreak
        '''
        beambreak:DigitalInput = DigitalInput(channel)
        return Beambreak(lambda: beambreak.get(), beambreak.close)
    
    @staticmethod
    def none() -> "Beambreak":
        '''
        Generates a beambreak that does not contain hardware. This beambreak will always return true.
        '''
        return Beambreak(lambda: True, lambda: None)
    
    @Log
    def get(self) -> bool:
        '''
        - `RETURNS` the value of the beambreak; true for unbroken, false for broken
        '''
        return self._beambreak()
    
    def close(self) -> None:
        '''
        Closes all resources as necessary
        '''
        self._close()
