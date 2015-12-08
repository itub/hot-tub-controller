class Status(object):

    def __init__(self):
        self.heater = 0
        self.pump1 = 0
        self.pump2 = 0
        self.tempIn = 25
        self.tempOut = 25
        self.tempAir = 25

    def to_jsonable(self):
        return {
            'heater': self.heater,
            'pump1': self.pump1,
            'pump2': self.pump2,
            'tempIn': self.tempIn,
            'tempOut': self.tempOut,
            'tempAir': self.tempAir,
        }
