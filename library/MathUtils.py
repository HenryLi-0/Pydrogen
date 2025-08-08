from wpimath.units import *
from wpimath.geometry import Rotation2d
import math

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
    kPerMinuteToPerSecond = 60
    kPerSecondToPerMinute = 1/kPerMinuteToPerSecond

class Vector:
    '''
    vector! because i [do stuff] with both direction and magnitude. oh yeah!
    '''
    def __init__(self, *args):
        self.storage = args
        self.size = len(args)
    def get(self, row:int) -> float:
        return self.storage[row]
    def times(self, value:float) -> "Vector":
        return self.__class__(*[x*value for x in self.storage])
    def div(self, value:float) -> "Vector":
        return self.__class__(*[x/value for x in self.storage])
    def plus(self, vec:"Vector") -> "Vector":
        if self.size == vec.size:
            return self.__class__(*[self.storage[i] + vec.storage[i] for i in range(self.size)])
        else: raise TypeError("Different vector sizes, can't add!")
    def minus(self, vec:"Vector") -> "Vector":
        if self.size == vec.size:
            return self.__class__(*[self.storage[i] - vec.storage[i] for i in range(self.size)])
        else: raise TypeError("Different vector sizes, can't subtract!")
    def dot(self, other:"Vector"):
        if self.size == other.size:
            dot = 0.0
            for i in range(self.size):
                dot += self.get(i) * other.get(i)
            return dot
        else: raise TypeError("Different vector sizes, can't get dot!")
    def norm(self) -> float:
        return math.sqrt(self.dot(self))
    def unit(self) -> "Vector":
        return self.div(self.norm())
    def projection(self, other:"Vector") -> "Vector":
        return self.times(self.dot(other)).div(other.dot(other))


class VectorN2(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)
