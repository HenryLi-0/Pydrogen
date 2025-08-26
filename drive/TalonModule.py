from wpimath.units import *
from library.MathUtils import *
from library.FaultLogger import *
from constants import DRIVE_CANIVORE
from constants import ODOMETRY_PERIOD
from constants import PERIOD
from library.LoggingUtils import *
from drive.ModuleIO import ModuleIO

from phoenix6.base_status_signal import BaseStatusSignal
from phoenix6.status_code import StatusCode
from phoenix6.configs import TalonFXConfiguration
from phoenix6.controls import PositionVoltage
from phoenix6.controls import VelocityVoltage
from phoenix6.hardware import CANcoder
from phoenix6.hardware import ParentDevice
from phoenix6.hardware import TalonFX
from phoenix6.signals import FeedbackSensorSourceValue
from phoenix6.signals import InvertedValue
from phoenix6.signals import NeutralModeValue
from wpimath.controller import SimpleMotorFeedforwardMeters # TODO chceck if units are meters vs. radians
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition
from wpimath.kinematics import SwerveModuleState
from library.TalonUtils import * 
from drive.DriveConstants import ControlMode
from drive.DriveConstants import FFConstants
from drive.DriveConstants import ModuleConstants


class TalonModule(ModuleIO):
    def __init__(self, drivePort:int, turnPort:int, sensorID:int, angularOffset:Rotation2d, ff:FFConstants, name:str, invert:bool):
        # drive motor
        self.driveMotor:TalonFX = TalonFX(drivePort, DRIVE_CANIVORE) # Kraken X60
        self.driveFF:SimpleMotorFeedforwardMeters = SimpleMotorFeedforwardMeters(ff.kS, ff.kV, ff.kA)
        
        # turn motor
        self.turnMotor:TalonFX = TalonFX(turnPort, DRIVE_CANIVORE) # Kraken X60
        self.encoder:CANcoder = CANcoder(sensorID, DRIVE_CANIVORE)

        self.velocityOut = VelocityVoltage(0)
        self.rotationsIn = PositionVoltage(0)


        self.setpoint:SwerveModuleState = SwerveModuleState()

        self.lastRotation:Rotation2d


        # init drive motor
        talonDriveConfig:TalonFXConfiguration = TalonFXConfiguration()
        talonDriveConfig.motor_output.neutral_mode = NeutralModeValue.BRAKE
        talonDriveConfig.feedback.sensor_to_mechanism_ratio = ModuleConstants.Driving.GEARING / ModuleConstants.Driving.CIRCUMFERENCE # meters
        talonDriveConfig.current_limits.stator_current_limit = ModuleConstants.Driving.STATOR_LIMIT # amps

        talonDriveConfig.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE if invert else InvertedValue.COUNTER_CLOCKWISE_POSITIVE

        talonDriveConfig.slot0.k_p = ModuleConstants.Driving.PID.P
        talonDriveConfig.slot0.k_i = ModuleConstants.Driving.PID.I
        talonDriveConfig.slot0.k_d = ModuleConstants.Driving.PID.D
        
        # init turn motor
        talonTurnConfig:TalonFXConfiguration = TalonFXConfiguration()
    
        talonTurnConfig.motor_output.neutral_mode = NeutralModeValue.BRAKE
        talonTurnConfig.motor_output.inverted = InvertedValue.CLOCKWISE_POSITIVE if invert else InvertedValue.COUNTER_CLOCKWISE_POSITIVE

        talonTurnConfig.feedback.sensor_to_mechanism_ratio = ModuleConstants.Turning.CANCODER_GEARING
        talonTurnConfig.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANCODER
        talonTurnConfig.feedback.feedback_remote_sensor_id = sensorID

        talonTurnConfig.closed_loop_general.continuous_wrap = True

        talonTurnConfig.slot0.k_p = ModuleConstants.Turning.PID.P
        talonTurnConfig.slot0.k_i = ModuleConstants.Turning.PID.I
        talonTurnConfig.slot0.k_d = ModuleConstants.Turning.PID.D

        talonTurnConfig.current_limits.stator_current_limit = ModuleConstants.Turning.CURRENT_LIMIT # amps

        for i in range(5):
            success:StatusCode = self.driveMotor.configurator.apply(talonDriveConfig)
            if success.is_ok(): break
        
        for i in range(5):
            success:StatusCode = self.turnMotor.configurator.apply(talonTurnConfig)
            if success.is_ok(): break
        
        # reduces update frequency on unnecessary signals
        # only reset on robot restart and redeploy or calling motor.resetSignalFrequencies()
        ParentDevice.optimize_bus_utilization_for_all(self.driveMotor, self.turnMotor)

        BaseStatusSignal.set_update_frequency_for_all(
            1 / ODOMETRY_PERIOD, # seconds
            self.driveMotor.get_position(),
            self.driveMotor.get_velocity(),
            self.turnMotor.get_position(),
            self.turnMotor.get_velocity()
        )

        BaseStatusSignal.set_update_frequency_for_all(
            1 / PERIOD, # seconds
            self.driveMotor.get_motor_voltage(),
            self.turnMotor.get_motor_voltage()
        )

        FaultLogger.registerTalon(self.driveMotor)
        FaultLogger.registerTalon(self.turnMotor)
        FaultLogger.registerCANcoder(self.encoder)

        TalonUtils.addMotor(self.driveMotor)
        TalonUtils.addMotor(self.turnMotor)

        self.resetEncoders()

        self.thisName:str = name
    
    def name(self) -> str:
        return self.thisName
    
    def setDriveVoltage(self, voltage:float) -> None:
        self.driveMotor.setVoltage(voltage)
    
    def setTurnVoltage(self, voltage:float) -> None:
        self.turnMotor.setVoltage(voltage)
    
    def drivePosition(self) -> float:
        return self.driveMotor.get_position().value_as_double

    def driveVelocity(self) -> float:
        return self.driveMotor.get_velocity().value_as_double
    
    def rotation(self) -> Rotation2d:
        self.lastRotation = Rotation2d.fromRotations(self.turnMotor.get_position().value_as_double)
        return self.lastRotation
    
    def state(self) -> SwerveModuleState:
        return SwerveModuleState(self.driveVelocity(), self.rotation())

    def position(self) -> SwerveModulePosition:
        return SwerveModulePosition(self.driveVelocity(), self.rotation())

    def desiredState(self) -> SwerveModuleState:
        return self.setpoint
    
    def resetEncoders(self) -> None:
        self.driveMotor.set_position(0)
    
    def setDriveSetpoint(self, velocity:float) -> None:
        self.driveMotor.set_control(
            self.velocityOut.with_velocity(velocity).with_feed_forward(self.driveFF.calculate(velocity)))

    def setTurnSetpoint(self, angle:Rotation2d) -> None:
        self.turnMotor.set_control(self.rotationsIn.with_position(angle.radians() * Convert.kRadiansToRotations).with_slot(0))

    def updateSetpoint(self, setpoint:SwerveModuleState, mode:ControlMode) -> None:
        currentRotation:Rotation2d = self.rotation()
        # Optimize the reference state to avoid spinning further than 90 degrees
        setpoint.optimize(currentRotation)
        # scale setpoint by cos of turning error to reduce tread wear
        setpoint.cosineScale(currentRotation)

        if mode == ControlMode.OPEN_LOOP_VELOCITY:
            self.setDriveVoltage(self.driveFF.calculate(setpoint.speed)) # meters per second
        else:
            self.setDriveSetpoint(setpoint.speed) # meters per second
        
        self.setTurnSetpoint(setpoint.angle)
        self.setpoint = setpoint
    
    def updateInputs(self, angle:Rotation2d, voltage:float) -> None:
        self.setpoint.angle = angle
        self.setDriveVoltage(voltage)
        self.setTurnSetpoint(angle)
    
    def close(self) -> None:
        self.turnMotor.close()
        self.driveMotor.close()
