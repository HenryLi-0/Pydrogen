from wpimath.geometry import Rotation2d
from wpimath.geometry import Rotation3d
from library.MathUtils import VectorN2


class GyroIO:
  '''Generalized gyroscope.'''
  def calibrate(self) -> None:
    '''Calibrates the gyroscope. Pigeon2 does not need to do anything here.'''
    pass

  def rate(self) -> float:
    '''Returns the rate of rotation.'''
    pass

  def rotation2d(self) -> Rotation2d:
    '''Returns the heading of the robot as a Rotation2d.'''
    return self.rotation3d().toRotation2d()

  def rotation3d(self) -> Rotation3d:
    '''Returns the heading of the robot as a Rotation3d.'''
    pass

  def acceleration() -> VectorN2:
    '''Returns the acceleration of the robot as a Vector.'''
    pass

  def reset(heading:Rotation2d) -> None:
    '''Resets heading to 0.'''
    pass
