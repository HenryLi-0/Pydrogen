import wpilib
from commands2 import CommandScheduler

class CommandRobot(wpilib.TimedRobot):
    '''
    [ref](https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/lib/CommandRobot.java)
    A command robot.
    '''
    def __init__(self, period = 0.02):
        super().__init__(period)
    
    def robotPeriodic(self):
        CommandScheduler.getInstance().run()

    def _simulationPeriodic(self):
        pass

    def disabledPeriodic(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopPeriodic(self):
        pass

    def testPeriodic(self):
        pass

    def testInit(self):
        CommandScheduler.cancelAll()