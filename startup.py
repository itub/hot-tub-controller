#!/usr/bin/env python

import cherrypy
from cherrypy.lib.static import serve_file

import json
from status import Status
from controller import Controller


class HotTubServer(object):

    def __init__(self):
        self.status = Status()
        self.controller = Controller()

    @cherrypy.expose
    def index(self):
        return serve_file('/home/pi/hot-tub-controller/index.html',
                          'text/html')

    @cherrypy.expose
    def current(self):
        return json.dumps(self.status.to_jsonable(), indent=4)

    @cherrypy.expose
    def heater_on(self):
        self.status.heater = 1
        self.controller.heater_on()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def heater_off(self):
        self.status.heater = 0
        self.controller.heater_off()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def pump1_low(self):
        self.status.pump1 = 1
        self.controller.pump1_low()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def pump1_high(self):
        self.status.pump1 = 2
        self.controller.pump1_high()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def pump1_off(self):
        self.status.pump1 = 0
        self.controller.pump1_off()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def pump2_off(self):
        self.status.pump2 = 0
        self.controller.pump2_off()
        return json.dumps(self.status.to_jsonable())

    @cherrypy.expose
    def pump2_on(self):
        self.status.pump2 = 1
        self.controller.pump2_on()
        return json.dumps(self.status.to_jsonable())


if __name__ == '__main__':
    cherrypy.quickstart(HotTubServer(),
                        '/',
                        '/home/pi/hot-tub-controller/server.conf')
