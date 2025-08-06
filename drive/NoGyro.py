from wpimath.geometry import Rotation2d
from wpimath.geometry import Rotation3d
from library.MathUtils import VectorN2
from drive.GyroIO import GyroIO

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/drive/GyroIO.java
'''

class NoGyro(GyroIO):
    '''GyroIO implementation for nonexistent gyro'''
    def __init__(self):
        self.rotation:Rotation3d = Rotation3d()

    def rate(self) -> float:
        return 0

    def rotation3d(self) -> Rotation3d:
        return self.rotation

    def acceleration(self) -> VectorN2:
        return VectorN2(0, 0)
