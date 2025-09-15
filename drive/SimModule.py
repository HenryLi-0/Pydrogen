from wpimath.units import *
from library.MathUtils import Convert
from math import pi

from drive.ModuleIO import ModuleIO

from wpimath.controller import PIDController
from wpimath.controller import SimpleMotorFeedforwardMeters # TODO check meters vs radians
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition
from wpimath.kinematics import SwerveModuleState
from wpimath.system.plant import DCMotor
from wpimath.system.plant import LinearSystemId
from wpilib.simulation import DCMotorSim
import constants
from drive.DriveConstants import ControlMode
from drive.DriveConstants import ModuleConstants


'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/drive/SimModule.java
'''


class SimModule(ModuleIO):
    def __init__(self, name:str):
        self.drive:DCMotorSim = DCMotorSim(
            LinearSystemId.DCMotorSystem(
                ModuleConstants.Driving.FRONT_LEFT_FF.kV,
                ModuleConstants.Driving.FRONT_LEFT_FF.kA
            ),
            DCMotor.krakenX60(1))
        
        self.driveFeedback:PIDController = PIDController(
            ModuleConstants.Driving.PID.P,
            ModuleConstants.Driving.PID.I,
            ModuleConstants.Driving.PID.D
        )

        self.driveFF:SimpleMotorFeedforwardMeters = SimpleMotorFeedforwardMeters(
            ModuleConstants.Driving.FRONT_LEFT_FF.kS,
            ModuleConstants.Driving.FRONT_LEFT_FF.kV,
            ModuleConstants.Driving.FRONT_LEFT_FF.kA
        )

        self.turn:DCMotorSim = DCMotorSim(
            ModuleConstants.Turning.PID.P,
            ModuleConstants.Turning.PID.I,
            ModuleConstants.Turning.PID.D
        )

        self.turnFeedback:PIDController = PIDController(
            ModuleConstants.Turning.PID.P,
            ModuleConstants.Turning.PID.I,
            ModuleConstants.Turning.PID.D
        )

        self.setpoint:SwerveModuleState = SwerveModuleState()

        self.thisName = name

        self.turnFeedback.enableContinuousInput(-pi, pi)
    
    def name(self) -> str:
        return self.thisName
    
    def setDriveVoltage(self, voltage:float) -> None:
        self.drive.setInputVoltage(voltage)
        self.drive.update(Constants.PERIOD)
    
    def setTurnVoltage(self, voltage:float) -> None:
        self.turn.setInputVoltage(voltage)
        self.turn.update(Constants.PERIOD)
    
    def drivePosition(self) -> float:
        return self.drive.getAngularPositionRotations() * Convert.kRotationsToRadians
    
    def driveVelocity(self) -> float:
        return self.drive.getAngularVelocityRPM() * Convert.kRotationsToRadians * Convert.kPerMinuteToPerSecond

    def rotation(self) -> Rotation2d:
        return Rotation2d.fromRotations(self.turn.getAngularPositionRotations())
    
    def state(self) -> SwerveModuleState:
        return SwerveModuleState(self.driveVelocity(), self.rotation())
    
    def position(self) -> SwerveModulePosition:
        return SwerveModulePosition(self.driveVelocity(), self.rotation())
    
    def desiredState(self) -> SwerveModuleState:
        return self.setpoint
    
    def resetEncoders(self) -> None:
        self.drive.setState(0, 0)
        self.turn.setState(0, 0)

    def setDriveSetpoint(self, velocity:float) -> None:
        self.setDriveVoltage(
            self.driveFeedback.calculate(self.driveVelocity(), velocity) + self.driveFF.calculate(velocity)
        )

    def setTurnSetpoint(self, angle:Rotation2d) -> None:
        self.setTurnVoltage(self.turnFeedback.calculate(self.rotation().radians(), angle.radians()))

    def updateSetpoint(self, setpoint:SwerveModuleState, mode:ControlMode) -> None:
        # Optimize the reference state to avoid spinning further than 90 degrees
        setpoint.optimize(self.rotation())
        # Scale setpoint by cos of turning error to reduce tread wear
        setpoint.cosineScale(self.rotation())

        if mode == ControlMode.OPEN_LOOP_VELOCITY:
            self.setDriveVoltage(self.driveFF.calculate(setpoint.speed))
        else:
            self.setDriveSetpoint(setpoint.speed)
        
        self.setTurnSetpoint(setpoint.angle)
        self.setpoint = setpoint

    def updateInputs(self, angle:Rotation2d, voltage:float) -> None:
        self.setpoint.angle = angle

        turnVoltage:float = self.turnFeedback.calculate(self.rotation().radians(), self.setpoint.angle.radians())

        self.setDriveVoltage(voltage)
        self.setTurnVoltage(turnVoltage)
