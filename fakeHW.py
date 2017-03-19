#!/usr/bin/env python

"""
These are fake HW interfaces for testing
"""
import platform
import os
if platform.system().lower() == 'linux' and 'CI' not in os.environ:
	from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	import RPi.GPIO as GPIO

else:
	class GPIO(object):
		IN = True
		OUT = False
		BCM = True
		LOW = 0
		def __init__(self): print('dummy GPIO')
		@staticmethod
		def setwarnings(a): pass
		@staticmethod
		def setmode(a): pass
		@staticmethod
		def setup(a, b): pass
		@staticmethod
		def input(a): return 1
		@staticmethod
		def output(a, b): pass
		@staticmethod
		def cleanup(): pass

	class MCP230XX(object):  # mux
		def __init__(self, a, b, c): pass
		def write8(self, a): print('mux wrote:', a)
		def config(self, a, b): pass

	class PWM(object):  # motors
		def __init__(self, a, b): pass
		def start(self, a): pass
		def stop(self): pass
		def ChangeDutyCycle(self, a): print('ChangeDutyCycle', a)
