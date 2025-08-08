from wpimath.units import *
from library.MathUtils import Convert
from library.MathUtils import KRotation2d
from math import pi
from math import sqrt

from wpimath.geometry import Rotation2d
from wpimath.geometry import Rotation3d
from wpimath.geometry import Translation2d

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/drive/DriveConstants.java
'''

'''
Constants for our 2025 Swerve X2t drivetrain! All fields in this file should be updated for the
current robot configuration!
'''

class ControlMode:
    '''The type of control loop to use when controlling a module's drive motor.'''
    CLOSED_LOOP_VELOCITY = 0
    OPEN_LOOP_VELOCITY = 1

# TODO kinda memory inefficient? (this is supposed to mimic a record)
class FFConstants:
  def __init__(self, kS:float, kV:float, kA:float):
    self.kS = kS
    self.kV = kV
    self.kA = kA

class ModuleType:
    '''The type of modules being used.'''
    TALON = 0 # Kraken X60 Drive, Kraken X60 Turn
    SPARK = 1 # NEO Vortex Drive, NEO 550 Turn

# TODO: Change central drivetrain constants as needed.

# The type of module on the chassis
TYPE:ModuleType = ModuleType.TALON

class Assisted:
  # The angle between the velocity and the displacement from a target, above which the robot will
  # not use assisted driving to the target. (the driver must be driving in the general direction
  # of the assisted driving target.)
  DRIVING_THRESHOLD:radians = radians(pi/6) 

  # The input of the joystick beyond which the assisted driving will not control the rotation of
  # the swerve.
  ROTATING_THRESHOLD:float = 0.02

class Skid:
  # TODO: find a value (3 is currently random, should change)
  THRESHOLD:meters_per_second = meters_per_second(3)

# The control loop used by all of the modules when driving
DRIVE_MODE = ControlMode.OPEN_LOOP_VELOCITY

# Rate at which sensors update periodicially
SENSOR_PERIOD:seconds = seconds(0.02)

# Distance between centers of right and left wheels on robot
TRACK_WIDTH:meters = meters(0.5715)
# Distance between front and back wheels on robot
WHEEL_BASE:meters = meters(0.5715)
# The radius of any swerve wheel
WHEEL_RADIUS:inches = inches(1.5)
# Distance from the center to any wheel of the robot
# TODO check if this errors
RADIUS:meters = (TRACK_WIDTH/2)*sqrt(2)
# Coefficient of friction between the drive wheel and the carpet.
WHEEL_COF:float = 1.0
# Robot width with bumpers
CHASSIS_WIDTH:inches = inches(32.645)

# Maximum achievable translational and rotation velocities and accelerations of the robot.
MAX_SPEED:meters_per_second = meters_per_second(5)
MAX_ACCEL:meters_per_second_squared = meters_per_second_squared(40)
MAX_SKID_ACCEL:meters_per_second_squared = meters_per_second_squared(38) # TODO: Tune
MAX_TILT_ACCEL:meters_per_second_squared = meters_per_second_squared(12) # TODO: Tune
MAX_ANGULAR_SPEED:radians_per_second = radians_per_second(MAX_ACCEL / RADIUS)
MAX_ANGULAR_ACCEL:radians_per_second_squared = radians_per_second_squared(MAX_ACCEL / RADIUS)

# Arbitrary max rotational velocity for the driver to effectively control the robot
TELEOP_ANGULAR_SPEED:radians_per_second = radians_per_second(2 * pi)

MODULE_OFFSET:list[Translation2d] = [
  Translation2d(WHEEL_BASE / 2, TRACK_WIDTH /  2), # front left
  Translation2d(WHEEL_BASE / 2, TRACK_WIDTH / -2), # front right
  Translation2d(WHEEL_BASE /-2, TRACK_WIDTH /  2), # rear left
  Translation2d(WHEEL_BASE /-2, TRACK_WIDTH / -2)  # rear right
]

# angular offsets of the modules, since we use absolute encoders
# ignored (used as 0) in simulation because the simulated robot doesn't have offsets
ANGULAR_OFFSETS:list[Rotation2d] = [
  KRotation2d.kZero, # front left
  KRotation2d.kZero, # front right
  KRotation2d.kZero, # rear left
  KRotation2d.kZero  # rear right
]

GYRO_OFFSET:Rotation3d = Rotation3d(0, 0, pi)

# TODO: Change ALL characterization constants for each unique robot as needed.
class Translation:
  P:float = 4.0
  I:float = 0.0
  D:float = 0.05

  TOLERANCE:meters = meters(1 * Convert.kCentimetersInMeters)

class Rotation:
  P:float = 4.5
  I:float = 0.0
  D:float = 0.05

  TOLERANCE:degrees = degrees(2)

class ModuleConstants:
  COUPLING_RATIO:float = 0
  
  class Driving:
    CIRCUMFERENCE:meters = WHEEL_RADIUS * 2 * pi

    GEARING:float = 5.68

    STATOR_LIMIT:amperes = amperes(80) # 120A max slip current
    SUPPLY_LIMIT:amperes = amperes(70)

    # these factors are for SparkModule only!
    POSITION_FACTOR:meters = CIRCUMFERENCE * GEARING
    VELOCITY_FACTOR:radians_per_second = radians_per_second(POSITION_FACTOR * Convert.kPerMinuteToPerSecond)

    CURRENT_LIMIT:amperes = amperes(50)
    
    class PID:
      P:float = 3.2
      I:float = 0.0
      D:float = 0.0
    
    FRONT_LEFT_FF:FFConstants = FFConstants(0.23328, 2.0243, 0.045604)
    FRONT_RIGHT_FF:FFConstants = FFConstants(0.21459, 2.0025, 0.094773)
    REAR_LEFT_FF:FFConstants = FFConstants(0.14362, 2.0942, 0.21547)
    REAR_RIGHT_FF:FFConstants = FFConstants(0.15099, 1.9379, 0.30998)

    FF_CONSTANTS:list[FFConstants] = [
      FRONT_LEFT_FF, FRONT_RIGHT_FF, REAR_LEFT_FF, REAR_RIGHT_FF
    ]

  class Turning:
    GEARING:float = 12.1
    CANCODER_GEARING:float = 1

    CURRENT_LIMIT:amperes = amperes(20)

    class PID:
      P:float = 50
      I:float = 0.0
      D:float = 0.05
    
    # system constants only used in simulation
    class FF:
      S:float = 0.30817
      V:float = 0.55
      A:float = 0.03


