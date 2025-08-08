from phoenix6.status_signal import StatusSignal
from phoenix6.hardware import CANcoder
from phoenix6.hardware import TalonFX
# import com.reduxrobotics.sensors.canandgyro.Canandgyro;
# import com.revrobotics.REVLibError;
# import com.revrobotics.spark.SparkBase;
# import com.studica.frc.AHRS;
from phoenix6.hardware import Pigeon2
from hal import PowerDistributionFaults
from ntcore import NetworkTable
from ntcore import NetworkTableInstance
from ntcore import StringArrayPublisher
from wpilib import DriverStation
from wpilib import DutyCycleEncoder
from wpilib import PowerDistribution
from typing import Callable, Optional
# import org.photonvision.PhotonCamera;
from ports import Ports

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/lib/FaultLogger.java
'''

class FaultType:
  INFO = 0
  WARNING = 1
  ERROR = 2

# TODO kinda memory inefficient? (this is supposed to mimic a record)
class Fault:
  def __init__(self, name:str, description:str, typ:FaultType):
    self.name = name
    self.desc = description
    self.typ = typ
  def toString(self) -> str:
    return self.name + ": " + self.desc
    
class Alerts:
  table:NetworkTable = None
  errors:StringArrayPublisher = None
  warnings:StringArrayPublisher = None
  infos:StringArrayPublisher = None
  def __init__(base:NetworkTable, name:str):
    Alerts.table = base.getSubTable(name)
    Alerts.table.getStringTopic(".type").publish().set("Alerts")
    Alerts.errors = Alerts.table.getStringArrayTopic("errors").publish()
    Alerts.warnings = Alerts.table.getStringArrayTopic("warnings").publish()
    Alerts.infos = Alerts.table.getStringArrayTopic("infos").publish()

  def set(faults:list[Fault]) -> None:
    Alerts.errors.set(FaultLogger.filteredStrings(faults, FaultType.ERROR))
    Alerts.warnings.set(FaultLogger.filteredStrings(faults, FaultType.WARNING))
    Alerts.infos.set(FaultLogger.filteredStrings(faults, FaultType.INFO))

  def reset() -> None:
    Alerts.errors.close()
    Alerts.warnings.close()
    Alerts.infos.close()
    Alerts.table.getStringArrayTopic("errors").publish()
    Alerts.table.getStringArrayTopic("warnings").publish()
    Alerts.table.getStringArrayTopic("infos").publish()
        

class FaultLogger:
  '''
  FaultLogger allows for faults to be logged and displayed.

  faulatawelrlogeger
  '''
  # DATA
  faultReporters:list[Callable[[], Optional[Fault]]] = []
  activeFaults:set[Fault] = []
  totalFaults:set[Fault] = []

  # NETWORK TABLES
  base:NetworkTable = NetworkTableInstance.getDefault().getTable("Faults");
  activeAlerts:Alerts = Alerts(base, "Active Faults")
  totalAlerts:Alerts = Alerts(base, "Total Faults")

  @staticmethod
  def update() -> None:
    '''Polls registered fallibles. This method should be called periodically.'''
    for fault in FaultLogger.faultReporters:
      temp:Optional[Fault] = fault()
      if temp != None:
        FaultLogger.reportFault(temp)

    for fault in FaultLogger.activeFaults:
      FaultLogger.totalFaults.append(fault)
    
    FaultLogger.activeAlerts.set(FaultLogger.activeFaults)
    FaultLogger.totalAlerts.set(FaultLogger.totalFaults)

    FaultLogger.activeFaults.clear()
  
  @staticmethod
  def clear() -> None:
    '''Clears total faults.'''
    FaultLogger.totalFaults.clear()
    FaultLogger.activeFaults.clear()

    FaultLogger.totalAlerts.reset()
    FaultLogger.activeAlerts.reset()
  
  @staticmethod
  def unregisterAll() -> None:
    '''Clears fault suppliers.'''
    FaultLogger.faultReporters.clear()
  
  @staticmethod
  def getActiveFaults() -> set[Fault]:
    '''
    Returns the set of all current faults.
    - `RETURNS` The set of all current faults.
    '''
    return FaultLogger.activeFaults
  
  @staticmethod
  def getTotalFaults() -> set[Fault]:
    '''
    Returns the set of all total faults.
    - `RETURNS` The set of all total faults.
    '''
    return FaultLogger.totalFaults
  
  @staticmethod
  def reportFault(fault:Fault) -> None:
    '''
    Reports a fault.
    - `fault` The fault to report.
    '''
    FaultLogger.activeFaults.add(fault)
    print(fault.toString())
    # TODO DriverStation.reportError and DriverStation.reportWarning don't seem to exist???
    # switch (fault.type) {
    #   case ERROR -> DriverStation.reportError(fault.toString(), false);
    #   case WARNING -> DriverStation.reportWarning(fault.toString(), false);
    #   case INFO -> System.out.println(fault.toString());
    # }

  @staticmethod
  def reportFaultData(name:str, desc:str, typ:FaultType) -> None:
    '''
    Reports a fault.
    - `name` The name of the fault.
    - `desc` The description of the fault.
    - `typ` The type of the fault.
    '''
    FaultLogger.reportFault(Fault(name, desc, typ))

  @staticmethod
  def reportFaultConditional(condition:bool, fault:Fault) -> bool:
    '''
    Conditionally reports a fault and returns the condition.
    - `condition` The condition
    - `fault` The fault
    - `RETURNS` The value of the condition
    '''
    if condition:
      FaultLogger.reportFault(fault)
    return condition
  
  @staticmethod
  def registerSupplier(supplier:Callable[[], Optional[Fault]]) -> None:
    '''
    Registers a new fault supplier.
    - `supplier` A supplier of an optional fault.
    '''
    FaultLogger.faultReporters.add(supplier)
  
  @staticmethod
  def registerSupplierData(condition:Callable[[], bool], name:str, desc:str, typ:FaultType) -> None:
    '''
    Registers a new fault supplier.

    - `condition` A callable that returns whether a failure is occuring.
    - `description` The failure's description.
    - `type` The type of failure.
    '''
    FaultLogger.registerSupplier(lambda: Fault(name, desc, typ) if condition() else None)
  
  '''
  TODO REV python lib currently not official yet.

  /**
   * Registers fault suppliers for a CAN-based Spark motor controller.
   *
   * @param spark The Spark Max or Spark Flex to manage.
   */
  public static void register(SparkBase spark) {
    register(
        () -> spark.getFaults().other,
        SparkUtils.name(spark),
        "other strange error",
        FaultType.ERROR);
    register(
        () -> spark.getFaults().motorType,
        SparkUtils.name(spark),
        "motor type error",
        FaultType.ERROR);
    register(
        () -> spark.getFaults().sensor, SparkUtils.name(spark), "sensor error", FaultType.ERROR);
    register(() -> spark.getFaults().can, SparkUtils.name(spark), "CAN error", FaultType.ERROR);
    register(
        () -> spark.getFaults().temperature,
        SparkUtils.name(spark),
        "temperature error",
        FaultType.ERROR);
    register(
        () -> spark.getFaults().gateDriver,
        SparkUtils.name(spark),
        "gate driver error",
        FaultType.ERROR);
    register(
        () -> spark.getFaults().escEeprom,
        SparkUtils.name(spark),
        "escEeprom? error",
        FaultType.ERROR);
    register(
        () -> spark.getFaults().firmware,
        SparkUtils.name(spark),
        "firmware error",
        FaultType.ERROR);
    register(
        () -> spark.getMotorTemperature() > 100,
        SparkUtils.name(spark),
        "motor above 100°C",
        FaultType.WARNING);
  }
  '''
  
  @staticmethod
  def registerDutyCycleEncoder(encoder:DutyCycleEncoder):
    '''
    Registers fault suppliers for a duty cycle encoder.
    - `encoder` The duty cycle encoder to manage.
    '''
    FaultLogger.registerSupplierData(
      lambda: not(encoder.isConnected()),
      "Duty Cycle Encoder [{}]".format(encoder.getSourceChannel()),
      "disconnected",
      FaultType.ERROR
    )

  '''
  TODO check for studica python support
  /**
   * Registers fault suppliers for a NavX.
   *
   * @param ahrs The NavX to manage.
   */
  public static void register(AHRS ahrs) {
    register(() -> !ahrs.isConnected(), "NavX", "disconnected", FaultType.ERROR);
  }
  '''

  '''
  TODO check for redux python support

  /**
   * Registers Alerts for faults of a Redux Boron CANandGyro.
   *
   * @param canandgyro The Redux Boron CANandGyro to manage.
   */
  public static void register(Canandgyro canandgyro) {
    register(() -> !canandgyro.isConnected(), "CANandGyro", "disconnected", FaultType.ERROR);
    register(
        () -> canandgyro.getActiveFaults().accelerationSaturation(),
        "CANandGyro",
        "acceleration saturated",
        FaultType.WARNING);
    register(
        () -> canandgyro.getActiveFaults().angularVelocitySaturation(),
        "CANandGyro",
        "angular velocity saturated",
        FaultType.WARNING);
    register(
        () -> canandgyro.getActiveFaults().calibrating(),
        "CANandGyro",
        "calibrating",
        FaultType.WARNING);
    register(
        () -> canandgyro.getActiveFaults().canGeneralError(),
        "CANandGyro",
        "general CAN error",
        FaultType.ERROR);
    register(
        () -> canandgyro.getActiveFaults().canIDConflict(),
        "CANandGyro",
        "CAN ID conflict",
        FaultType.ERROR);
    register(
        () -> canandgyro.getActiveFaults().outOfTemperatureRange(),
        "CANandGyro",
        "temperature error",
        FaultType.ERROR);
    register(
        () -> canandgyro.getActiveFaults().powerCycle(),
        "CANandGyro",
        "power cycling",
        FaultType.WARNING);
  }
  '''

  @staticmethod
  def registerPowerDistribution(powerDistribution:PowerDistribution) -> None:
    '''
    Registers fault suppliers for a power distribution hub/panel.
    - `powerDistribution` The power distribution to manage.
    '''
    '''
    TODO what (powerdistribution)
    
    var fields = PowerDistributionFaults.class.getFields();
    for (Field fault : fields) {
      register(
          () -> {
            try {
              if (fault.getBoolean(powerDistribution.getFaults())) {
                return Optional.of(
                    new Fault("Power Distribution", fault.getName(), FaultType.ERROR));
              }
            } catch (Exception e) {
            }
            return Optional.empty();
          });
    }
    '''
    pass

  '''
  TODO check for photonvision python support

  /**
   * Registers fault suppliers for a camera.
   *
   * @param camera The camera to manage.
   */
  public static void register(PhotonCamera camera) {
    register(
        () -> !camera.isConnected(),
        "Photon Camera [" + camera.getName() + "]",
        "disconnected",
        FaultType.ERROR);
  }
  '''

  @staticmethod
  def registerCANcoder(cancoder:CANcoder) -> None:
    '''
    Registers fault suppliers for a CANcoder.
    - `cancoder` The CANcoder to manage.
    '''
    # TODO add ports
    nickname:str = Ports.idToName[cancoder.device_id]
    FaultLogger.registerSupplierData(
      lambda: cancoder.get_fault_bad_magnet().value(),
      "CANcoder {}".format(nickname),
      "The magnet distance is not correct or magnet is missing.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
        lambda: cancoder.get_fault_boot_during_enable().value(),
        "CANcoder {}".format(nickname),
        "Device boot while detecting the enable signal.",
        FaultType.WARNING
    )
    FaultLogger.registerSupplierData(
        lambda: cancoder.get_fault_hardware().value(),
        "CANcoder {}".format(nickname),
        "Hardware fault occurred.",
        FaultType.WARNING
    )
    FaultLogger.registerSupplierData(
        lambda: cancoder.get_fault_undervoltage().value(),
        "CANcoder {}".format(nickname),
        "Device supply voltage dropped to near brownout levels.",
        FaultType.WARNING
    )
  
  @staticmethod
  def registerTalon(talon:TalonFX) -> None:
    '''
    Registers fault suppliers for a talon.
    - `talon` The talon to manage.
    '''
    nickname:str = Ports.idToName[talon.device_id()]
    FaultLogger.registerSupplierData(
      lambda: not(talon.is_connected()),
      "Talon {}".format(nickname),
      "disconnected",
      FaultType.ERROR
    )
    regFault = lambda f,d: FaultLogger.registerSupplierData(
      lambda: f(),
      "Talon {}".format(nickname),
      d,
      FaultType.ERROR
    )

    regFault(talon.get_fault_hardware, "Hardware fault occured.")
    regFault(talon.get_fault_ProcTemp, "Processor temperature exceeded limit")
    regFault(talon.get_fault_device_temp, "Device temperature exceeded limit")
    regFault(talon.get_fault_undervoltage, "Device supply voltage dropped to near brownout levels")
    regFault(talon.get_fault_boot_during_enable, "Device boot while detecting the enable signal")
    regFault(talon.get_fault_unlicensed_feature_in_use, "An unlicensed feature is in use, device may not behave as expected.")
    regFault(talon.get_fault_bridge_brownout, "Bridge was disabled most likely due to supply voltage dropping too low.")
    regFault(talon.get_fault_remote_sensor_reset, "The remote sensor has reset.")
    regFault(talon.get_fault_missing_differential_fx, "The remote Talon FX used for differential control is not present on CAN Bus.")
    regFault(talon.get_fault_remote_sensor_pos_overflow, "The remote sensor position has overflowed.")
    regFault(talon.get_fault_over_supply_v, "Supply Voltage has exceeded the maximum voltage rating of device.")
    regFault(talon.get_fault_unstable_supply_v, "Supply Voltage is unstable.")
    regFault(talon.get_fault_reverse_hard_limit, "Reverse limit switch has been asserted.  Output is set to neutral.")
    regFault(talon.get_fault_forward_hard_limit, "Forward limit switch has been asserted.  Output is set to neutral.")
    regFault(talon.get_fault_reverse_soft_limit, "Reverse soft limit has been asserted.  Output is set to neutral.")
    regFault(talon.get_fault_forward_soft_limit, "Forward soft limit has been asserted.  Output is set to neutral.")
    regFault(talon.get_fault_remote_sensor_data_invalid, "The remote sensor's data is no longer trusted.")
    regFault(talon.get_fault_fused_sensor_out_of_sync, "The remote sensor used for fusion has fallen out of sync to the local sensor.")
    regFault(talon.get_fault_stator_curr_limit, "Stator current limit occured.")
    regFault(talon.get_fault_supply_curr_limit, "Supply current limit occured.")
    regFault(talon.get_fault_using_fused_cancoder_while_unlicensed, "Using Fused CANcoder feature while unlicensed. Device has fallen back to remote CANcoder.")

  '''
  TODO REV python lib currently not official yet.
  
  /**
   * Reports REVLibErrors from a spark.
   *
   * <p>This should be called immediately after any call to the spark.
   *
   * @param spark The spark to report REVLibErrors from.
   * @return If the spark is working without errors.
   */
  public static boolean check(SparkBase spark) {
    REVLibError error = spark.getLastError();
    return check(spark, error);
  }

  /**
   * Reports REVLibErrors from a spark.
   *
   * <p>This should be called immediately after any call to the spark.
   *
   * @param spark The spark to report REVLibErrors from.
   * @param error Any REVLibErrors that may be returned from a method for a spark.
   * @return If the spark is working without errors.
   */
  public static boolean check(SparkBase spark, REVLibError error) {
    if (error != REVLibError.kOk) {
      report(SparkUtils.name(spark), error.name(), FaultType.ERROR);
      return false;
    }
    return true;
  }
  '''

  @staticmethod
  def registerPigeon(pigeon:Pigeon2) -> None:
    '''
    Registers fault suppliers for a pigeon2.
    - `pigeon` The pigeon2 to manage.
    '''
    nickname:str = Ports.idToName[pigeon.device_id]
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_boot_during_enable().value(),
      "CANcoder {}".format(nickname),
      "Device boot while detecting the enable signal.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_boot_into_motion().value(),
      "CANcoder {}".format(nickname),
      "Motion detected during bootup.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_bootup_accelerometer().value(),
      "CANcoder {}".format(nickname),
      "Accelerometer bootup checks failed.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_bootup_gyroscope().value(),
      "CANcoder {}".format(nickname),
      "Gyroscope bootup checks failed.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_bootup_magnetometer().value(),
      "CANcoder {}".format(nickname),
      "Magnetometer bootup checks failed.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_data_acquired_late().value(),
      "CANcoder {}".format(nickname),
      "Motion stack data acquisition was slower than expected.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_field().value(),
      "CANcoder {}".format(nickname),
      "Integer representing all fault flags reported by the device.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_hardware().value(),
      "CANcoder {}".format(nickname),
      "Hardware fault occured.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_loop_time_slow().value(),
      "CANcoder {}".format(nickname),
      "Motion stack loop time was slower than expected.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_saturated_accelerometer().value(),
      "CANcoder {}".format(nickname),
      "Accelerometer values are saturated.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_saturated_gyroscope().value(),
      "CANcoder {}".format(nickname),
      "Gyroscope values are saturated.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_saturated_magnetometer().value(),
      "CANcoder {}".format(nickname),
      "Magnetometer values are saturated.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_undervoltage().value(),
      "CANcoder {}".format(nickname),
      "Device supply voltage dropped to near brownout levels.",
      FaultType.ERROR
    )
    FaultLogger.registerSupplierData(
      lambda: pigeon.get_fault_unlicensed_feature_in_use().value(),
      "CANcoder {}".format(nickname),
      "An unlicensed feature is in use, device may not behave as expected.",
      FaultType.ERROR
    )



  @staticmethod
  def filteredStrings(faults:set[Fault], typ:FaultType) -> list[str]:
    '''
    Returns an array of descriptions of all faults that match the specified type.
    - `type` The type to filter for.
    - `RETURNS` An array of description strings.
    '''
    return [fault.toString() for fault in faults if fault.typ == typ]