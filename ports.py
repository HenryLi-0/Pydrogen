'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/robot/Ports.java
'''

class Ports:
    # TODO: Add and change all ports as needed.

    class OI:
        OPERATOR:int = 0
        DRIVER:int = 1
    
    class Drive:
        GYRO:int = 20
        FRONT_LEFT_DRIVE:int = 11
        REAR_LEFT_DRIVE:int = 10
        FRONT_RIGHT_DRIVE:int = 12
        REAR_RIGHT_DRIVE:int = 13

        FRONT_LEFT_TURNING:int = 15
        REAR_LEFT_TURNING:int = 14
        FRONT_RIGHT_TURNING:int = 16
        REAR_RIGHT_TURNING:int = 17

        # For Talons
        FRONT_LEFT_CANCODER:int = 5
        REAR_LEFT_CANCODER:int = 7
        FRONT_RIGHT_CANCODER:int = 6
        REAR_RIGHT_CANCODER:int = 8

    class LEDs:
        LED_PORT:int = 9

    idToName:dict[int, str] = {
        Drive.FRONT_LEFT_DRIVE: "FL drive",
        Drive.REAR_LEFT_DRIVE: "RL drive",
        Drive.FRONT_RIGHT_DRIVE: "FR drive",
        Drive.REAR_RIGHT_DRIVE: "RR drive",

        Drive.FRONT_LEFT_TURNING: "FL turn",
        Drive.REAR_LEFT_TURNING: "RL turn",
        Drive.FRONT_RIGHT_TURNING: "FR turn",
        Drive.REAR_RIGHT_TURNING: "RR turn",

        # For Talons
        Drive.FRONT_LEFT_CANCODER: "FL cancoder",
        Drive.REAR_LEFT_CANCODER: "RL cancoder",
        Drive.FRONT_RIGHT_CANCODER: "FR cancoder",
        Drive.REAR_RIGHT_CANCODER: "RR cancoder"
    }