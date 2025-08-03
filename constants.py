from wpimath.units import *

from wpimath.geometry import Rotation2d
from wpilib import DriverStation

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/Constants.java
'''

class Constants:
    '''
    Constants is a globally accessible class for storing immutable values.
    
    It is advised to statically import this class (or one of its inner classes) wherever the
    constants are needed, to reduce verbosity.
    '''

    # TODO: Modify as needed.

    @staticmethod
    def alliance() -> DriverStation.Alliance:
        '''Returns the robot's alliance.'''
        return DriverStation.getAlliance()
    
    @staticmethod
    def allianceRotation() -> Rotation2d:
        return Rotation2d.fromRotations(0 if Constants.alliance() == DriverStation.Alliance.kBlue else 0.5)
    
    class RobotType:
        '''Defines the various types the robot can be. Useful for only using select subsystems.'''
        FULL = -1
        CHASSIS = 1
        NONE = 0
    
    # The current robot state, as in the type. Remember to update!
    ROBOT_TYPE:RobotType = RobotType.FULL

    # States if we are in tuning mode. Ideally, keep it at false when not used.
    TUNING:bool = False

    # TODO: UPDATE ALL OF THESE VALUES.
    # TODO: is this cursed? idk the wpilib python equivalent of java units library
    class Robot:
        '''Describes physical properites of the robot.'''
        MASS:kilograms = kilograms(25)
        MOI:kilogram_square_meters = kilogram_square_meters(0.2)
    
    PERIOD:seconds = seconds(0.02) # roborio tickrate (s)
    ODOMETRY_PERIOD:seconds = seconds(1.0 / 20.0) # 4 ms (speedy!) TODO: check
    DEADBAND:float = 0.15
    '''
    TODO implement driveconstants

      public static final double MAX_RATE =
      DriveConstants.MAX_ACCEL.baseUnitMagnitude()
          / DriveConstants.MAX_ANGULAR_SPEED.baseUnitMagnitude();
    '''

    SLOW_SPEED_MULTIPLIER:float = 0.33
    FULL_SPEED_MULTIPLIER:float = 1.0

    # The name of seperate canivore, set to rio if no seperate canivore
    DRIVE_CANIVORE:str = "drivetrain"
