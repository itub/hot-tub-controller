import RPi.GPIO as GPIO


class Controller(object):

    PUMP1_LOW = 11
    PUMP1_HIGH = 12
    PUMP2 = 13
    HEATER = 7

    def __init__(self):
        GPIO.setup([self.PUMP1_LOW, self.PUMP1_HIGH, self.PUMP2, self.HEATER],
                   GPIO.OUT, initial=GPIO.LOW)

    def pump1_off(self):
        GPIO.output([self.PUMP1_LOW, self.PUMP1_HIGH], GPIO.LOW)

    def pump1_low(self):
        GPIO.output([self.PUMP1_LOW, self.PUMP1_HIGH], (GPIO.HIGH, GPIO.LOW))

    def pump1_high(self):
        GPIO.output([self.PUMP1_LOW, self.PUMP1_HIGH], (GPIO.LOW, GPIO.HIGH))

    def pump2_off(self):
        GPIO.output(self.PUMP2, GPIO.LOW)

    def pump2_on(self):
        GPIO.output(self.PUMP2, GPIO.HIGH)

    def heater_off(self):
        GPIO.output(self.HEATER, GPIO.LOW)

    def heater_on(self):
        GPIO.output(self.HEATER, GPIO.HIGH)
