from library.MathUtils import *
from library.MathUtils import KRotation2d
from constants import alliance

# import edu.wpi.first.math.VecBuilder;
# import edu.wpi.first.math.Vector;
from wpimath.geometry import Pose2d
from wpimath.geometry import Pose3d
from wpimath.geometry import Rotation2d
from wpimath.geometry import Rotation3d
from wpimath.geometry import Transform2d
from wpimath.geometry import Translation2d
# import edu.wpi.first.math.numbers.N2;
from wpilib import DriverStation

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/FieldConstants.java
'''

# TODO: is this cursed? idk the wpilib python equivalent of java units library

# Origin at corner of blue alliance side of field
LENGTH:centimeters = centimeters(1755)
WIDTH:centimeters = centimeters(805)

def inField(pose:Pose3d) -> bool:
    '''Returns whether the provided position is within the boundaries of the field.'''
    return pose.X() > 0 and pose.X() < LENGTH * Convert.kCentimetersInMeters and pose.Y() > 0 and pose.Y() < WIDTH * Convert.kCentimetersInMeters

def fromPolarCoords(magnitude:float, direction:Rotation2d) -> list[float]:
    '''
    Creates a Vector from polar coordinates.
    - `magnitude` The magnitude of the vector.
    - `direction` The direction of the vector.
    - `RETURNS` A vector (2 float list) from the given polar coordinates.
    '''
    return [magnitude * direction.cos(), magnitude * direction.sin()]

def allianceReflect(pose:Pose2d) -> Pose2d:
    '''
    Rotates a pose 180* with respect to the center of the field, effectively swapping alliances.

    This only works for rotated reflect fields like Reefscape, not mirrored fields like Crescendo.

    - `pose` The pose being reflected.
    - `RETURNS` The reflected pose.
    '''
    # TODO: check if this is wonky
    return pose if alliance() == DriverStation.Alliance.kBlue else Pose2d(
        pose.translation()
            .rotateAround(
                Translation2d(LENGTH*Convert.kCentimetersInMeters/2, WIDTH*Convert.kCentimetersInMeters/2),
                KRotation2d.k180deg),
        pose.rotation().__add__(KRotation2d.k180deg))

def reflectDistance(blueDist:meters) -> "meters":
    '''
    Reflects width-wise distances through the middle of the field if the alliance is red, otherwise
    does nothing
    - `blueDist` The input distance, usually for the blue alliance, IN METERS.
    - `RETURNS` A reflected distance, only if the alliance is red, IN METERS.
    '''
    return blueDist if alliance() == DriverStation.Alliance.kBlue else WIDTH*Convert.kCentimetersInMeters-blueDist

def allianceFromPose(pose:Pose2d) -> DriverStation.Alliance:
    return DriverStation.Alliance.kRed if pose.X() > LENGTH*Convert.kCentimetersInMeters/2 else DriverStation.Alliance.kBlue

def strafe(distance:meters) -> Transform2d:
    '''
    A transform that will translate the pose robot-relative right by a certain distance. Negative
    distances will move the pose left.

    - `distance` The distance that the pose will be moved.
    - `RETURNS` A transform to strafe a pose.
    '''
    
    return Transform2d(
        Transform2d(distance, KRotation2d.kCW_90deg), KRotation2d.kZero)

def advance(distance:meters) -> Transform2d:
    '''
    A transform that will translate the pose robot-relative forward by a certain distance. Negative
    distances will move the pose backward.

    - `distance` The distance that the pose will be moved.
    - `RETURNS` A transform to move a pose forward.
    '''
    return Transform2d(
        Translation2d(distance, KRotation2d.kZero), KRotation2d.kZero)

# List field constants below!


