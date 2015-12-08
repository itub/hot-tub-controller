#!/usr/bin/env python

import cherrypy
from cherrypy.lib.static import serve_file

import RPi.GPIO as GPIO
import json
from adc import ADCReader
from status import Status
import thermistor
from controller import Controller


def validate_password(realm, user, password):
    with open('/home/pi/users.json') as fd:
        users = json.loads(fd.read())
    return unicode(user) in users and users[unicode(user)] == unicode(password)

class HotTubServer(object):

    def __init__(self):
        self.adc = ADCReader()
        self.status = Status()
        self.controller = Controller()

    @cherrypy.expose
    def index(self):
        return serve_file('/home/pi/hot-tub-controller/index.html',
                          'text/html')

    def _validatepassword(self, user, password):
        return True

    @cherrypy.expose
    def current(self):
        self.status.tempAir = thermistor.adc_value_to_F(self.adc.readadc(7))
        self.status.tempIn = thermistor.adc_value_to_F(self.adc.readadc(3))
        self.status.tempOut = thermistor.adc_value_to_F(self.adc.readadc(5))
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


def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())


if __name__ == '__main__':
    try:
        GPIO.cleanup()
    except:
        pass
    GPIO.setmode(GPIO.BOARD)
    with open('/home/pi/hot-tub-controller/server.conf') as fd:
        config = json.loads(fd.read(), object_hook=ascii_encode_dict)
    config['/']['tools.auth_basic.checkpassword'] = validate_password
    cherrypy.quickstart(HotTubServer(), '/', config)
