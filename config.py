import json


class Config(object):

    def __init__(self):
        self.two_speed_pump = False
        self.second_pump = False
        self.read()

    def read(self):
        try:
            with open('/home/pi/config.json') as fd:
                config = json.loads(fd.read())
            self.two_speed_pump = config['two_speed_pump']
            self.second_pump = config['second_pump']
        except Exception as err:
            print err

    def to_jsonable(self):
        return {'two_speed_pump': self.two_speed_pump,
            'second_pump': self.second_pump}
