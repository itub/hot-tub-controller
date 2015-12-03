# hot-tub-controller
Raspberry Pi web enabled hot tub controller, supporting a heater (on/off or pool/spa control), air and water temperature thermistors, one two-speed pump, a second pump, (with hardware schematic). Includes freeze protection setting (run pump based on low air temperature) and daily filtering. Can continue to run pump (cool-down) for 15 minutes after heater is turned off.

Some design/development notes...

I built this project first years ago with an Arduino and WiFi (WiFly) shield. It worked well, as the Arduino has plenty of GPIO pins and enough analog pins to deal with everything. The most painful part was the Wi-Fi shield, and it's (very) beta supporting code. I originally build the controller so that it polled an external service (the cloud!) to get it's settings, and built an iOS application.

For various reasons (avoiding hosting fees among them), I decided to try this again, but change a few things to see if it worked out better:
1) Use a Raspberry Pi instead, and build everything in Python
2) Don't use a cloud service -- just host a web server on the Raspberry Pi itself. This requires forwarding a port and using dynamic DNS services to get it working, but that turns out to be Not a Big Deal.

Circuit notes:
- I'm using high voltage SSR relays for 220V pumps and sanitizer. 5 of them (one for main pump low speed, one for main pump high, two paired up for the second pump, and one for the sanitizer).
- I measured the current draw with a multimeter with 3.3V applied to one of the SSR relays. 6 mA. The spec on Raspberry Pi GPIO current limits isn't very public, but most links I found say 50mA total is the limit, and 5mA per pin is reasonable. Assuming a 3.0V turn-on on the SSR, adding a 47 ohm resistor in series would reduce the current to 5.4 mA and we would not require external transistors.
- The heater switch uses an SPDT relay. This requires 5V turn-on current, so it needs a transistor driven from a 3.3V GPIO pin just for that, if not for current draw.
- The Raspberry Pi does't have analog inputs. So we need an ADC. The MCP3008 gives us 8 analog inputs and an SPI interface that uses up four GPIO pins. We'll use 3 of the inputs: water temperature into the heater, water temperature out of the heater, and ambient air temperature. The thermistor are brass threaded thermistors with 10k resistance at 77F. Doing some simple math, you can add a 10k resistor in series and give it a supply voltage and measure the middle. The result is about 0.16 degree F accuracy with the 10-bit values returned from the MCP3008, and a very simple circuit.



