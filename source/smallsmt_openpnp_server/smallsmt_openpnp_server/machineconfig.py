import configtreeview


class CoordInfo:
    def __init__(self):
        self.Cnv_PulseToMm_f8 = 1
        self.Min_f3 = 0
        self.Max_f3 = 200.0

class MachineRange:
    def __init__(self):
        # Base coordinates
        self.X = CoordInfo()
        self.Y = CoordInfo()

        # Heads
        self.Z1 = CoordInfo()
        self.C1 = CoordInfo()
        self.Z2 = CoordInfo()
        self.C2 = CoordInfo()
        self.Z3 = CoordInfo()
        self.C3 = CoordInfo()
        self.Z4 = CoordInfo()
        self.C4 = CoordInfo()

        # Feeders
        self.F1W = CoordInfo()
        self.F2N = CoordInfo()
        self.F3E = CoordInfo()
        self.F4S = CoordInfo()


class FeedTemplate:
    def __init__(self):
        self.Cnv_PulseToMm_f8 = 1
        self.Min_f3 = 0
        self.Max_f3 = 200.0



class FeedTemplates:
    def __init__(self,cnt):
        self.position_f = []
        for i in range(cnt):
            self.position_f.append(0)


class SpeedTemplate:
    def __init__(self,cnt):
        self.position_f = []
        for i in range(cnt):
            self.position_f.append(0)




class SideFeeder:
    def __init__(self,cnt):
        self.position_f = []
        for i in range(cnt):
            self.position_f.append(0)



class GlobalConfig:
    def __init__(self):
        self.Axes = MachineRange()


class MachineConfig:
    def __init__(self):
        self.Feder1W = SideFeeder(32)
        self.Feder2N = SideFeeder(32)
        self.Feder3E = SideFeeder(32)