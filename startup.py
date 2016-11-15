#!/usr/bin/env python

import cherrypy
from cherrypy.lib.static import serve_file

import datetime
import RPi.GPIO as GPIO
import json
from adc import ADCReader
from config import Config
from status import Status
import thermistor
from controller import Controller
import threading
from threading import Timer

from twilio.rest import TwilioRestClient

def validate_password(realm, user, password):
    with open('/home/pi/users.json') as fd:
        users = json.loads(fd.read())
    return unicode(user) in users and users[unicode(user)] == unicode(password)


class HotTubServer(object):

    def __init__(self):
        self.adc = ADCReader()
        self.config = Config()
        self.status = Status()
        self.controller = Controller()
        self.freeze_status = 0
        self.filter_status = 0
        self.last_alert = datetime.datetime.utcfromtimestamp(0)
        self.adclock = threading.Lock()
        Timer(30.0, self.filter_timer).start()
        self.twilio_heartbeat()

    @cherrypy.expose
    def index(self):
        return serve_file('/home/pi/hot-tub-controller/index.html',
                          'text/html')

    def twilio_heartbeat(self):
        try:
            with open('/home/pi/alerts.json') as fd:
                alerts = json.loads(fd.read())
            if not alerts['number']:
                return
            for number in alerts['number'].split(',')[:1]:
                client = TwilioRestClient(alerts['twilio_sid'], alerts['twilio_token'])
                client.messages.create(
                    to = number,
                    from_ = alerts['twilio_number'],
                    body = "Daily hot tub text alert test."
                    )
        finally:
            Timer(24 * 60 * 60, self.twilio_heartbeat).start()

    def filter_timer(self):
        try:
            self.current()
            self.config.read()
            with open('/home/pi/filter.json') as fd:
                filter_settings = json.loads(fd.read())
            now = datetime.datetime.now()
            seconds = (now.hour * 3600) + (now.minute * 60) + now.second
            # freeze control checks
            self.filter_status = 1 if (filter_settings['start'] <= seconds and
                  filter_settings['end'] >= seconds) else 0
            self.freeze_status = 1 if self.status.tempAir < 37.0 else 0
            if self.freeze_status == 1 and self.status.pump1 == 0:
                self.controller.pump1_low()
            elif self.filter_status == 1 and self.status.pump1 == 0:
                self.controller.pump1_low()
            elif self.status.pump1 == 0 and (not self.filter_status == 1) and (not self.freeze_status == 1):
                self.controller.pump1_off()
            with open('/home/pi/alerts.json') as fd:
                alerts = json.loads(fd.read())
            if self.status.tempIn < alerts['threshold'] and self.freeze_status == 1 and \
                (datetime.datetime.now() - self.last_alert).total_seconds() > 300:
                print "WARNING: WATER TEMPERATURE ALERT. POSSIBLE POWER OUTAGE."
                try:
                    if alerts['number']:
                        for number in alerts['number'].split(','):
                            client = TwilioRestClient(alerts['twilio_sid'], alerts['twilio_token'])
                            client.messages.create(
                                to = number,
                                from_ = alerts['twilio_number'],
                                body = "WARNING - hot tub freeze alarm: {:.1f}F".format(
                                     self.status.tempIn)
                            )
                    self.last_alert = datetime.datetime.now()
                except Exception as err:
                    print "Error sending SMS alert: {}".format(err)
        finally:
            Timer(30.0, self.filter_timer).start()

    @cherrypy.expose
    def getconfig(self):
        return json.dumps(self.config.to_jsonable(), indent=4)

    @cherrypy.expose
    def current(self):
        try:
            self.adclock.acquire(True)
            self.status.tempAir = thermistor.adc_value_to_F(self.adc.readadc(7))
            self.status.tempIn = thermistor.adc_value_to_F(self.adc.readadc(5))
            self.status.tempOut = thermistor.adc_value_to_F(self.adc.readadc(3))
            status = self.status.to_jsonable()
            status['freeze_status'] = self.freeze_status
            status['filter_status'] = self.filter_status
            return json.dumps(status, indent=4)
        finally:
            self.adclock.release()

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
