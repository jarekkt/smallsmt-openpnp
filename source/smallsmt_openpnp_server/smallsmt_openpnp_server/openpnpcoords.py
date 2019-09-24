from struct import *
import math
import re


class SingleCoord:

    def __init__(self):
        self.home()

    def home(self):
        self.value = 0
        self.steps = 0
        self.steps_delta = 0

    def moveTo(self,range,newValue):
         outOfRange = 0
         # Do not touch Nan values
         if math.isNan(newValue):
             return 0

         # Make sure we are in range
         if (newValue > range.Max_f3):
             newValue = range.Max_f3
             outOfRange = 1

         if (newValue < range.Min_f3):
             newValue = range.Min_f3
             outOfRange = 1

         newSteps = math.floor(newValue / range.Cnv_PulseToMm_f8)
         self.steps_delta = self.steps - newSteps
         self.steps = newSteps

         return outOfRange

class OpenPnpCoordsSplitter:

    def __init__(self,text):
        self.splited = re.split('\(,\)',text)

    def toMove(self):
        move = {}
        move['cmd'] = self.splited[0]
        move['base'] = self.splited[1]
        move['X'] = self.splited[2]
        move['Y'] = self.splited[3]
        move['Z'] = self.splited[4]
        move['C'] = self.splited[5]

        return move

    def toActuatorRead(self):
        move = {}
        move['cmd'] = self.splited[0]
        move['actuator'] = self.splited[1]

    def toActuatorWrite(self):
        move = {}
        move['cmd'] = self.splited[0]
        move['actuator'] = self.splited[1]
        move['value'] = self.splited[2]

        return move

class OpenPnpCoords:

    def Home(self):
        self.X.home()
        self.Y.home()
        self.Z12.home()
        self.Z34.home()
        self.C1.home()
        self.C2.home()
        self.C3.home()
        self.C4.home()
        self.F1W.home()
        self.F2N.home()
        self.F3E.home()
        self.outOfRange = 0


    def MoveToInit(self):
        self.X.steps_delta = 0
        self.Y.steps_delta = 0
        self.Z12.steps_delta = 0
        self.Z34.steps_delta = 0
        self.C1.steps_delta = 0
        self.C2.steps_delta = 0
        self.C3.steps_delta = 0
        self.C4.steps_delta = 0
        self.F1W.steps_delta = 0
        self.F2N.steps_delta = 0
        self.F3E.steps_delta = 0

    def MoveToX(self,newValue):
        self.outOfRange += self.X.moveTo(self.range.X,newValue)

    def MoveToY(self,newValue):
        self.outOfRange += self.Y.moveTo(self.range.Y, newValue)

    def MoveToZ12(self,newValue):
        self.outOfRange += self.Z12.moveTo(self.range.Z12, newValue)

    def MoveToZ34(self,newValue):
        self.outOfRange += self.Z34.moveTo(self.range.Z34, newValue)

    def MoveToC1(self,newValue):
        self.outOfRange += self.C1.moveTo(self.range.C1, newValue)

    def MoveToC2(self,newValue):
        self.outOfRange += self.C2.moveTo(self.range.C2, newValue)

    def MoveToC3(self,newValue):
        self.outOfRange += self.C3.moveTo(self.range.C3, newValue)

    def MoveToC4(self,newValue):
        self.outOfRange += self.C4.moveTo(self.range.C4, newValue)

    def MoveToF1W(self,newValue):
        self.outOfRange += self.F1W.moveTo(self.range.F1W, newValue)

    def MoveToF2N(self,newValue):
        self.outOfRange += self.F2N.moveTo(self.range.F2N, newValue)

    def MoveToF3E(self,newValue):
        self.outOfRange += self.F3E.moveTo(self.range.F3E, newValue)

    def __init__(self,configRange):
        self.range = configRange

        self.X = SingleCoord()
        self.Y = SingleCoord()
        self.Z12 = SingleCoord()
        self.Z34 = SingleCoord()
        self.C1 = SingleCoord()
        self.C2 = SingleCoord()
        self.C3 = SingleCoord()
        self.C4 = SingleCoord()
        self.F1W = SingleCoord()
        self.F2N = SingleCoord()
        self.F3E = SingleCoord()
        self.outOfRange = 0
