import wpilib
from core import *
import threading

class RobotShooterPiston:
    def __init__(self):
        self.armTimer = wpilib.Timer()
        self.armTimer.Start()

        self.doRaise = False
        self.lowerTimer = wpilib.Timer()

        self.armDown = False
        #self.armDown = True # XXX for LAB TESTING ONLY

        self.mutex = threading.RLock()
        self.armThread = threading.Thread(target=self._ArmThread,
                name="ArmThread")
        self.armThread.start()

    def Init(self):
        self.armTimer.Reset()
 
    def Shoot (self):
        with self.mutex:
            Robot.shooterPiston.Set(wpilib.DoubleSolenoid.kReverse)
            wpilib.Wait(0.3)
            Robot.shooterPiston.Set(wpilib.DoubleSolenoid.kForward)

    def _ArmThread(self):
        while 1:
            with self.mutex:
                # handle raise commands
                if self.doRaise:
                    if Robot.elevation.IsArmUpOk():
                        Robot.shooterPiston.Set(wpilib.DoubleSolenoid.kForward)
                        self.armTimer.Reset()
                        self.doRaise = False

                # handle lower commands
                if self.lowerTimer.Get() > 0.3:
                    self.armDown = True
                    self.lowerTimer.Stop()
                    self.lowerTimer.Reset()

                # pulse latching pneumatics
                if self.armTimer.Get() > 0.2:
                    Robot.shooterPiston.Set(wpilib.DoubleSolenoid.kOff)
            wpilib.Wait(0.1)

