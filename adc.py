import RPi.GPIO as GPIO


class ADCReader(object):

    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler
    SPICLK = 18
    SPIMISO = 19
    SPIMOSI = 21
    SPICS = 23

    def __init__(self):
        # set up the SPI interface pins
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(self.SPICS, True)

        GPIO.output(self.SPICLK, False)  # start clock low
        GPIO.output(self.SPICS, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(self.SPIMOSI, True)
            else:
                    GPIO.output(self.SPIMOSI, False)
            commandout <<= 1
            GPIO.output(self.SPICLK, True)
            GPIO.output(self.SPICLK, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(self.SPICLK, True)
            GPIO.output(self.SPICLK, False)
            adcout <<= 1
            if (GPIO.input(self.SPIMISO)):
                adcout |= 0x1

        GPIO.output(self.SPICS, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
