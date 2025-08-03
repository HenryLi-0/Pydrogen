from wpimath.units import *
from wpimath.geometry import Rotation2d

'''
There is no Java version of this, this is just meant to add extra stuff 
that seem to be missing from the Python version, like some constants.
'''

class KRotation2d:
    '''
    Constants for Rotation2D's.
    '''
    kZero = Rotation2d.fromDegrees(0)
    k180deg = Rotation2d.fromDegrees(180)

    # TODO double check if Rotation2d.kCW_90deg is -90 degrees
    kCW_90deg = Rotation2d.fromDegrees(-90)

class Convert:
    '''
    Conversions meant to mimic the Java Units Library.
    '''
    kCentimetersInMeters = 0.01
    kMetersInCentimeters = 100