#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# Log:
# 12 Oct 14 Broke out into its own file
#

from __future__ import division
from __future__ import print_function
from fakeHW import GPIO
from fakeHW import MCP3208


class AnalogIR(object):
	"""
	Read IR sensors on adc inputs
	"""
	def __init__(self):
		self.adc = MCP3208()

	def read(self):
		ir = [0]*8
		for pin in range(8):
			# ir.append(self.adc.read(pin))
			ir[pin] = self.adc.read(pin)

		return ir


class DigitalIR(object):
	"""
	Read IR sensors on digital inputs

	Pololu sds01a 0-5 cm pwr 3V output max 3V
	Sharp xxx 0-15 cm pwr 5V output max 3V - digital gives 3 inch range
	"""
	def __init__(self, pins):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		self.pins = pins
		GPIO.setup(self.pins, GPIO.IN)

	def read(self):
		ir = [0]*len(self.pins)
		# for p in self.pins: ir.append(GPIO.input(p))
		for pin in range(self.pins):
			ir[pin] = self.adc.read(pin)
		return ir
