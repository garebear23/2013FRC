import wpilib
from core import *
import threading

class RobotHanger:
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
 
    def Raise(self):
       
        with self.mutex:
            self.doRaise = True
            self.armDown = False

    def Lower(self):
        with self.mutex:
            Robot.climbPiston.Set(wpilib.DoubleSolenoid.kReverse)
            self.armTimer.Reset()

        self.lowerTimer.Start()

    def IsDown(self):
        with self.mutex:
            return self.armDown

    def IsUp(self):
        with self.mutex:
            return not self.armDown

    def _ArmThread(self):
        while 1:
            with self.mutex:
                # handle raise commands
                if self.doRaise:
                    if Robot.elevation.IsArmUpOk():
                        Robot.climbPiston.Set(wpilib.DoubleSolenoid.kForward)
                        self.armTimer.Reset()
                        self.doRaise = False

                # handle lower commands
                if self.lowerTimer.Get() > 0.3:
                    self.armDown = True
                    self.lowerTimer.Stop()
                    self.lowerTimer.Reset()

                # pulse latching pneumatics
                if self.armTimer.Get() > 0.2:
                    Robot.climbPiston.Set(wpilib.DoubleSolenoid.kOff)
            wpilib.Wait(0.1)

