from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition
from wpimath.kinematics import SwerveModuleState
from drive.DriveConstants import ControlMode
from library.MathUtils import KRotation2d

from drive.ModuleIO import ModuleIO

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/drive/NoModule.java
'''

class NoModule(ModuleIO):

    def name(self) -> str:
        return "No Module"
    
    def drivePosition(self) -> float:
        return 0
    
    def driveVelocity(self) -> float:
        return 0

    def rotation(self) -> Rotation2d:
        return KRotation2d.kZero

    def state(self) -> SwerveModuleState:
        return SwerveModuleState()
    
    def position(self) -> SwerveModulePosition:
        return SwerveModulePosition()

    def desiredState(self) -> SwerveModuleState:
        return SwerveModuleState()
