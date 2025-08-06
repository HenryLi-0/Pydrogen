from wpimath.units import *
from library.FaultLogger import FaultLogger
from drive.GyroIO import GyroIO
from ports import Ports 

from phoenix6.hardware.pigeon2 import Pigeon2
from phoenix6.configs import Pigeon2Configuration
from library.MathUtils import VectorN2
from wpimath.geometry import Rotation2d
from wpimath.geometry import Rotation3d

'''
ref: NONE
(this was made for the reason that it would be nice to have a
gyro here, since redux and studica dont seem to support python
just yet)
'''

class PigeonGyro(GyroIO):
  '''GyroIO implementation for Pigeon2.'''
  def __init__(self):
    self.pigeon:Pigeon2 = Pigeon2(Ports.Drive.GYRO)
    
    config = Pigeon2Configuration()
    # TODO any pigeon configs here?
    self.pigeon.configurator.apply(config)
    self.pigeon.set_yaw(0, 0.1)
    self.pigeon.clear_sticky_faults()

    FaultLogger.registerPigeon(self.pigeon)

  def rate(self) -> float:
    return self.pigeon.get_angular_velocity_z_device().value_as_double()
  
  def rotation3d(self) -> Rotation3d:
    return self.pigeon.getRotation3d()
  
  def reset(self, heading:Rotation2d) -> None:
    self.pigeon.set_yaw(radiansToRotations(heading.radians()))

  def acceleration(self) -> VectorN2:
    return VectorN2(self.pigeon.get_acceleration_x(), self.pigeon.get_acceleration_y())
