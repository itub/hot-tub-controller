#!/usr/bin/env python

import cherrypy

import json
from status import Status
from controller import Controller


class HotTubServer(object):

    def __init__(self):
        self.status = Status()
        self.controller = Controller()

    def index(self):
        return "iTub controller v0.0.  Status: {}".format(
             json.dumps(self.status.to_jsonable(), indent=4))

    def heater_on(self):
        self.status.heater = 1
        self.controller.heater_on()
        return json.dumps(self.status.to_jsonable())

    def heater_off(self):
        self.status.heater = 0
        self.controller.heater_off()
        return json.dumps(self.status.to_jsonable())

    def pump1_low(self):
        self.status.pump1 = 1
        self.controller.pump1_low()
        return json.dumps(self.status.to_jsonable())

    def pump1_high(self):
        self.status.pump1 = 2
        self.controller.pump1_high()
        return json.dumps(self.status.to_jsonable())

    def pump1_off(self):
        self.status.pump1 = 0
        self.controller.pump1_off()
        return json.dumps(self.status.to_jsonable())

    def pump2_off(self):
        self.status.pump2 = 0
        self.controller.pump2_off()
        return json.dumps(self.status.to_jsonable())

    def pump2_on(self):
        self.status.pump2 = 1
        self.controller.pump2_on()
        return json.dumps(self.status.to_jsonable())

    index.exposed = True
    heater_on.exposed = True
    heater_off.exposed = True
    pump1_low.exposed = True
    pump1_high.exposed = True
    pump1_off.exposed = True
    pump2_off.exposed = True
    pump2_on.exposed = True

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HotTubServer())
