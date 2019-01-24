from struct import *
import binascii


class SmallSmtCoords:
    def add(self,delta):
        self.X = self.X + delta.X
        self.Y = self.Y + delta.Y
        self.Z1 = self.Z1 + delta.Z1
        self.Z2 = self.Z2 + delta.Z2
        self.Z3 = self.Z3 + delta.Z3
        self.Z4 = self.Z4 + delta.Z4
        self.C1 = self.C1 + delta.C1
        self.C2 = self.C2 + delta.C2
        self.C3 = self.C3 + delta.C3
        self.C4 = self.C4 + delta.C4
        self.W1 = self.W1 + delta.W1
        self.W2 = self.W2 + delta.W2
        self.W3 = self.W3 + delta.W3

    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Z1 = 0
        self.Z2 = 0
        self.Z3 = 0
        self.Z4 = 0
        self.C1 = 0
        self.C2 = 0
        self.C3 = 0
        self.C4 = 0
        self.W1 = 0
        self.W2 = 0
        self.W3 = 0


class SmallSmtPacket:
    # Base common packet definitions

    IDENTIFIER_QUESTION = 0
    IDENTIFIER_RESPONSE_OK = 1
    IDENTIFIER_RESPONSE_FAULT = 0xFF

    def __init__(self):
        self.databytes = bytearray()
        self.length = 0
        self.identifier = None
        self.data_type = None
        self.checksum = None
        self.bytes = None
        self.coordDelta = SmallSmtCoords()

    def prepare_packet(self, identifier, data_type, databytes):
        self.identifier = identifier
        self.data_type = data_type
        self.databytes = databytes
        self.encode_packet()

    def encode_packet(self):
        # Start character
        self.bytes.append(0xEE)
        self.length += 1
        # Message identifier
        self.bytes.append(self.identifier)
        self.length += 1
        # Data length
        self.bytes.append(len(self.databytes) + 2)
        # Data type
        self.bytes.append(self.data_type)
        # Data
        self.bytes.append(self.databytes)
        self.length += 2 + len(self.databytes)
        # Checksum
        self.checksum = self.checksumCalc(self.bytes, 2,self.length)
        self.bytes.append(self.checksum)
        self.length += 1
        # End characters
        self.bytes.append(0xFF)
        self.bytes.append(0xFC)
        self.bytes.append(0xFF)
        self.bytes.append(0xFF)
        self.length += 4

    def decodePacket(self, message):
        if len(message) < 7:
            raise Exception("Wrong message length")
        if message[0] != 0xEE:
            raise Exception("Wrong start character")
        self.identifier = message[1]
        self.data_type = message[2]
        self.length = len(message) - 7 # Note - no length field in messages from machine
        self.databytes = bytearray(self.length)
        for i in range(0, self.length):
            self.databytes[i] = message[3+i]
        self.checksum = message[len(message)-5]
        if self.checksum != self.checksumCalc(message,2,len(message)-5):
            raise Exception("Wrong checksum")
        if ((message[len(message)-1] != 0xFF) or (message[len(message)-2] != 0xFF) or
            (message[len(message)-3] != 0xFC) or (message[len(message)-4] != 0xFF)):
            raise Exception("Wrong stop characters")

    def checksumCalc(self,array,startIdx,endIdx):
        # Checksum by simple adding bytes
        chksum = 0
        for i in range(startIdx,endIdx):
            chksum += array[i];
        return (chksum & 0xff)

    def convertRange0_100ToByte(self,range0_100,min=1,max=255):
        value = (range0_100 * 255)/100
        if value < min:
            value = min
        elif value > max:
            value = max
        return int(value)

    def convertSteps(self,steps):
        # converts to unsigned 31 bit int, highest bit has the sign (step direction)
        sign = 0
        if steps < 0:
            sign = 1
            steps = -steps
        result = pack("<L",int(steps))
        if sign != 0:
            result[0] = result[0] | 0x80
        return bytearray(result)

    def convertRotation(self,steps):
        # converts to unsigned 15 bit int, highest bit has the sign (step direction)
        sign = 0
        if steps < 0:
            sign = 1
            steps = -steps
        result = pack("<H",int(steps))
        if sign != 0:
            result[0] = result[0] | 0x80
        return bytearray(result)

    def convertShort(self, val):
        # converts to unsigned 16 bit int
        sign = 0
        result = pack("<H", int(val))
        return bytearray(result)

    def convertLong(self, val):
        # converts to unsigned 32 bit int
        sign = 0
        result = pack("<L", int(val))
        return bytearray(result)

    def toString(self):
        return bytes.hex()


class SmallSmtCmd__Online(SmallSmtPacket):
    # Ping command
    CMD_ONLINE = 0x00

    def __init__(self):
        SmallSmtPacket.__init__(self)
        self.preparePacket(self.IDENTIFIER_QUESTION,self.CMD_ONLINE,None)


class SmallSmtCmd__Reset(SmallSmtPacket):
    # Reset command
    CMD_RESET = 0x02

    def __init__(self,axes):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(14)
        marker = 0x06  # According to doc anything non-zero
        if axes.find("X"):
            databytes[0] = marker
            databytes[1] = marker
        if axes.find("Y"):
            databytes[2] = marker
            databytes[3] = marker
        if axes.find("Z1"):
            databytes[4] = marker
            databytes[5] = marker
        if axes.find("Z2"):
            databytes[6] = marker
            databytes[7] = marker
        if axes.find("W1"):
            databytes[8] = marker
            databytes[9] = marker
        if axes.find("W2"):
            databytes[10] = marker
            databytes[11] = marker
        if axes.find("W3"):
            databytes[12] = marker
            databytes[13] = marker
        self.preparePacket(self.IDENTIFIER_QUESTION,self.CMD_RESET,databytes)

class SmallSmtCmd__ResetValves(SmallSmtPacket):
    # Reset command for valves for push feeder arms
    CMD_RESET = 0x02

    VALVE_NFEEDER = 0x06
    VALVE_WFEEDER = 0x05
    VALVE_EFEEDER = 0x07
    VALVE_SFEEDER = 0x0A

    def __init__(self, valve):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(valve)
        databytes.append(0x00)
        databytes.append(0x00)
        databytes.append(0x64)
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_RESET, databytes)

class SmallSmtCmd__Solenoid(SmallSmtPacket):
    # I/O control
    CMD_SOLENOID = 0x03

    PORT_VACUUM1 = 0x01
    PORT_VACUUM2 = 0x02
    PORT_VACUUM3 = 0x03
    PORT_VACUUM4 = 0x04
    PORT_WEST_FEEDER = 0x05
    PORT_NORTH_FEEDER = 0x06
    PORT_EAST_FEEDER = 0x07
    PORT_RESERVED1 = 0x08
    PORT_RESERVED2 = 0x09
    PORT_VIBRATION = 0x0A
    PORT_LIGHT1 = 0x0B
    PORT_LIGHT2 = 0x0C
    PORT_LIGHT3 = 0x0D

    def __init__(self,port,enable):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(2)
        databytes[0] = port
        if enable != 0:
            databytes[0] = 1
        else:
            databytes[0] = 0
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_SOLENOID, databytes)


class SmallSmtCmd__CameraMux(SmallSmtPacket):
    # Camera control
    CMD_VISUAL = 0x04

    CAM_DOWN = 0x01
    CAM_UP_LEFT = 0x02
    CAM_UP_RIGHT = 0x03

    def __init__(self,cameraId,brightness):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(2)
        databytes[0] = cameraId
        databytes[1] = self.convertRange0_100ToByte(brightness)
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_VISUAL, databytes)


class SmallSmtCmd__SpeedCoefficient(SmallSmtPacket):
    # Global speed control
    CMD_SPEED = 0x11

    def __init__(self,speedVal):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(1)
        databytes[0] = speedVal
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_SPEED, databytes)


class SmallSmtCmd__ReadVacum(SmallSmtPacket):
    # Read vacuum
    CMD_VACUUM = 0x15

    HEAD_NOZZLE1 = 0x01
    HEAD_NOZZLE2 = 0x02
    HEAD_NOZZLE3 = 0x03
    HEAD_NOZZLE4 = 0x04

    def __init__(self, head_nozzle):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(1)
        databytes[0] = head_nozzle
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_VACUUM, databytes)




class SmallSmtCmd__SmtMode(SmallSmtPacket):
    CMD_SMT = 0x60

    MODE_MANUAL = 0x00
    MODE_BEGIN = 0x01
    MODE_PAUSE = 0x02
    MODE_RECOVER = 0x03
    MODE_STOP = 0x04

    def __init__(self, mode):
        SmallSmtPacket.__init__(self)
        databytes = bytearray(1)
        databytes[0] = mode
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_SMT, databytes)



class SmallSmtCmd__Move(SmallSmtPacket):
    CMD_MOVEMENT = 0x61

    # Motor indexing
    MOTOR_XAXIS = 0x00
    MOTOR_YAXIS = 0x01

    MOTOR_ZAXIS1 = 0x02
    MOTOR_ZAXIS2 = 0x02
    MOTOR_ZAXIS3 = 0x03
    MOTOR_ZAXIS4 = 0x03

    MOTOR_AAXIS1 = 0x04
    MOTOR_AAXIS2 = 0x05
    MOTOR_AAXIS3 = 0x06
    MOTOR_AAXIS4 = 0x07

    MOTOR_WFEEDERWALKER = 0x08
    MOTOR_NFEEDERWALKER = 0x09
    MOTOR_EFEEDERWALKER = 0x0A


    def __init__(self, motor,steps,startSpeed,runSpeed):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(motor)
        databytes.append(self.convertSteps(steps))
        databytes.append(self.convertRange0_100ToByte(startSpeed))
        databytes.append(self.convertRange0_100ToByte(runSpeed))
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_MOVEMENT, databytes)


class SmallSmtCmd__MultiMove(SmallSmtPacket):
    # Multi XY A1 A2 A3 A4 movement

    CMD_MULTI_MOVEMENT = 0x65

    def __init__(self,
                 stepsX, startSpeedX, runSpeedX,
                 stepsY, startSpeedY, runSpeedY,
                 stepsA1,startSpeedA1,runSpeedA1,
                 stepsA2, startSpeedA2, runSpeedA2,
                 stepsA3, startSpeedA3, runSpeedA3,
                 stepsA4, startSpeedA4, runSpeedA4
                 ):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(self.convertSteps(stepsX))
        databytes.append(self.convertRange0_100ToByte(startSpeedX))
        databytes.append(self.convertRange0_100ToByte(runSpeedX))
        databytes.append(self.convertSteps(stepsY))
        databytes.append(self.convertRange0_100ToByte(startSpeedY))
        databytes.append(self.convertRange0_100ToByte(runSpeedY))
        databytes.append(self.convertRotation(stepsA1))
        databytes.append(self.convertRange0_100ToByte(startSpeedA1))
        databytes.append(self.convertRange0_100ToByte(runSpeedA1))
        databytes.append(self.convertRotation(stepsA2))
        databytes.append(self.convertRange0_100ToByte(startSpeedA2))
        databytes.append(self.convertRange0_100ToByte(runSpeedA2))
        databytes.append(self.convertRotation(stepsA3))
        databytes.append(self.convertRange0_100ToByte(startSpeedA3))
        databytes.append(self.convertRange0_100ToByte(runSpeedA3))
        databytes.append(self.convertRotation(stepsA4))
        databytes.append(self.convertRange0_100ToByte(startSpeedA4))
        databytes.append(self.convertRange0_100ToByte(runSpeedA4))
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_MULTI_MOVEMENT, databytes)


class SmallSmtCmd__FeederControl(SmallSmtPacket):
    # Embedded feeder control ( Yamaha has separate control )
    CMD_FEED = 0x66

    DIR_WESTFEEDER = 0x01
    DIR_NORTHFEEDER = 0x02
    DIR_EASTFEEDER = 0x03


    def __init__(self, dirFeeder,
                 steps,startSpeed,runSpeed,
                 openLength,closedLength,openCloseSpeedStart,openCloseSpeedRun,
                 feedTime,
                 pushCount):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(dirFeeder)
        databytes.append(self.convertSteps(steps))
        databytes.append(self.convertRange0_100ToByte(startSpeed))
        databytes.append(self.convertRange0_100ToByte(runSpeed))
        databytes.append(self.convertShort(openLength))
        databytes.append(self.convertShort(closedLength))
        databytes.append(self.convertRange0_100ToByte(openCloseSpeedStart))
        databytes.append(self.convertRange0_100ToByte(openCloseSpeedRun))
        databytes.append(self.convertShort(feedTime))
        databytes.append(pushCount)
        databytes.append(0x01)
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_FEED, databytes)


class SmallSmtCmd__FeederControlYamaha(SmallSmtPacket):
    # Embedded feeder control for Yamaha CL feeders
    CMD_FEED = 0x66

    DIR_SFEEDER = 0x0A

    def __init__(self,feederIndex, fedTimeUs):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(self.DIR_SFEEDER)
        databytes.append(self.convertLong(1<<feederIndex))
        databytes.append(self.convertLong(0))
        databytes.append(self.convertLong(0))
        databytes.append(self.convertShort(fedTimeUs))
        databytes.append(0x01) # push count
        databytes.append(feederIndex) # set feeder slot index
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_FEED, databytes)

class SmallSmtCmd__Pick(SmallSmtPacket):

    # Pick command
    CMD_PICK_UP = 0x67

    HEAD_ZAXIS1 = 0x02
    HEAD_ZAXIS2 = 0x02
    HEAD_ZAXIS3 = 0x03
    HEAD_ZAXIS4 = 0x03

    def __init__(self,zAxis,startSpeed,runSpeed,zSteps,nozzleNr,putDelay,vacumTestLevel):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(zAxis)
        databytes.append(self.convertSteps(zSteps))
        databytes.append(self.convertRange0_100ToByte(startSpeed))
        databytes.append(self.convertRange0_100ToByte(runSpeed))
        databytes.append(nozzleNr)
        databytes.append(self.convertShort(putDelay))
        databytes.append(vacumTestLevel)
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_PICK_UP, databytes)


class SmallSmtCmd__Place(SmallSmtPacket):
    # Place command
    CMD_PLACE = 0x68

    HEAD_ZAXIS1 = 0x02
    HEAD_ZAXIS2 = 0x02
    HEAD_ZAXIS3 = 0x03
    HEAD_ZAXIS4 = 0x03

    def __init__(self,zAxis, startSpeed,runSpeed,zSteps,zStepVacumShut,putDelay,vacumTestLevel):
        SmallSmtPacket.__init__(self)
        databytes = bytearray()
        databytes.append(zAxis)
        databytes.append(self.convertSteps(zSteps))
        databytes.append(self.convertRange0_100ToByte(startSpeed))
        databytes.append(self.convertRange0_100ToByte(runSpeed))
        databytes.append(self.convertSteps(zStepVacumShut))
        databytes.append(self.convertShort(putDelay))
        databytes.append(vacumTestLevel)
        self.preparePacket(self.IDENTIFIER_QUESTION, self.CMD_PLACE, databytes)

class SmallSmtCmd_Response(SmallSmtPacket):

    # Panel buttons definition
    PANEL_OFFLINE_COMMAND = 0x02
    PANEL_BUTTON_RIGHT = 0x39
    PANEL_BUTTON_DOWN = 0x37
    PANEL_BUTTON_UP = 0x36
    PANEL_BUTTON_LEFT = 0x38
    PANEL_BUTTON_MIDDLE = 0x35
    PANEL_BUTTON_START = 0x31
    PANEL_BUTTON_PAUSE_RESUME = 0x32
    PANEL_BUTTON_STOP = 0x33

    def __init__(self, incoming_bytes):
        SmallSmtPacket.__init__(self)
        self.decodePacket(incoming_bytes)



class SmallSmtProtocol:
    def __init__(self):
        pass






