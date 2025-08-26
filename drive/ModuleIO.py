from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition
from wpimath.kinematics import SwerveModuleState
from drive.DriveConstants import ControlMode
# TODO write drive constants

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/drive/ModuleIO.java
'''

class ModuleIO:
    '''Generalized hardware internals for a swerve module.'''

    def name(self) -> str:
        '''
        Returns the name of the swerve module (e.g. "FR" indicating the front right swerve module.)
        - `RETURNS` The name of the swerve module.
        '''
        pass

    def setDriveVoltage(self, voltage:float) -> None:
        '''
        Sets the drive voltage of the module.
        - `voltage` The voltage to input into the drive motor.
        '''
        pass

    def setTurnVoltage(self, voltage:float) -> None:
        '''
        Sets the turn voltage of the module.
        - `voltage` The voltage to input into the turn motor.
        '''
        pass
    
    def drivePosition(self) -> float:
        '''
        Returns the distance the wheel traveled.
        - `RETURNS` The drive encoder position value, in meters.
        '''
        pass
    
    def driveVelocity(self) -> float:
        '''
        Returns the current velocity of the wheel.
        - `RETURNS` The drive encoder velocity value, in meters / second.
        '''
        pass

    def rotation(self) -> Rotation2d:
        '''
        Returns the current angular position of the module.
        - `RETURNS` The adjusted turn encoder position value, in radians.
        '''
        pass

    def state(self) -> SwerveModuleState:
        '''
        Returns the current state of the module.
        - `RETURNS` The current state of the module.
        '''
        pass
    
    def position(self) -> SwerveModulePosition:
        '''
        Returns the current position of the module.
        - `RETURNS` The current position of the module.
        '''
        pass

    def desiredState(self) -> SwerveModuleState:
        '''
        Returns the desired position of the module.
        - `RETURNS` The desired position of the module.
        '''
        pass

    def resetEncoders(self) -> None:
        '''Resets all encoders.'''
        pass

    def setDriveSetpoint(self, velocity:float) -> None:
        '''
        Sets the setpoint value for the onboard drive motor's PID.
        - `velocity` The velocity setpoint.
        '''
        pass

    def setTurnSetpoint(self, angle:Rotation2d) -> None:
        '''
        Sets the setpoint value for the onboard turn motor's PID.
        - `angle` The angle setpoint.
        '''
        pass

    def updateSetpoint(self, setpoint:SwerveModuleState, mode:ControlMode) -> None:
        '''
        Updates controllers based on an optimized desired state and actuates the module accordingly.
        
        This method should be called periodically.
        
        - `setpoint` The desired state of the module.
        - `mode` The control mode to use when calculating drive voltage.
        '''
        pass

    def updateInputs(self, angle:Rotation2d, voltage:float) -> None:
        '''
        Updates the drive voltage and turn angle.

        This is useful for SysId characterization and should not be used otherwise.
        
        - `angle` The desired angle of the module.
        - `voltage` The voltage to supply to the drive motor.
        '''
        pass
    
    def close(self) -> None:
        # TODO autoclosable
        pass