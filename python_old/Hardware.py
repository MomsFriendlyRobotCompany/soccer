#!/usr/bin/python

from __future__ import division
from __future__ import print_function
import platform
import os
from mcp3208 import MCP3208

# if platform.system().lower() == 'linux' and 'CI' not in os.environ:
try:
	if 'CI' in os.environ or platform.system() != 'Linux':
		raise ImportError()
	# from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	import RPi.GPIO as GPIO
	from RPi.GPIO import PWM

except ImportError:
	from fake_rpi import GPIO
	from fake_rpi.PWM import PWM


class AnalogIR(object):
	"""
	Read IR sensors on adc inputs
	"""
	def __init__(self):
		self.adc = MCP3208()
		self.ir = {}
		for key in ['front', 'right', 'back', 'left']:
			self.ir[key] = 0

	def read(self):
		for pin, key in enumerate(self.ir):
			# ir.append(self.adc.read(pin))
			# print('read >>', pin, key)
			self.ir[key] = self.adc.read(pin)

		return self.ir


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


class MotorDriver(object):
	"""
	This uses RPI.GPIO
	"""
	STOP    = 0
	FORWARD = 1
	REVERSE = 2
	COAST   = 3

	def __init__(self, pwm0, pwm1, pwm2, pwm3, a0, b0, a1, b1):
		"""
		"""
		# self.mux = MCP230XX(0x20, 16, 1)
		#
		# for pin in range(0, 15):
		# 	self.mux.config(pin, GPIO.OUT)

		# this can be:
		# BOARD -> Board numbering scheme. The pin numbers follow the pin numbers on header P1.
		# BCM -> Broadcom chip-specific pin numbers.
		GPIO.setmode(GPIO.BCM)  # Pi cover uses BCM pin numbers, GPIO.BCM = 11
		GPIO.setup([pwm0, pwm1, pwm2, pwm3], GPIO.OUT)  # GPIO.OUT = 0

		freq = 100.0  # Hz
		self.motor0 = PWM(pwm0, freq)
		self.motor1 = PWM(pwm1, freq)
		self.motor2 = PWM(pwm2, freq)
		self.motor3 = PWM(pwm3, freq)

		self.motor0.start(0)
		self.motor1.start(0)
		self.motor2.start(0)
		self.motor3.start(0)

		self.ctl = [a0, b0, a1, b1]

		GPIO.setup([a0, b0, a1, b1], GPIO.OUT)  # GPIO.OUT = 0
		# self.a0 = a0
		# self.b0 = b0
		# self.a1 = a1
		# self.b1 = b1

		# GPIO.output(self.a0, GPIO.LOW)
		# GPIO.output(self.b0, GPIO.LOW)
		# GPIO.output(self.a1, GPIO.LOW)
		# GPIO.output(self.a1, GPIO.LOW)

		for pin in self.ctl:
			GPIO.output(pin, GPIO.LOW)

	def __del__(self):
		print('motor drive ... bye')
		self.allStop()
		self.motor0.stop()
		self.motor1.stop()
		self.motor2.stop()
		self.motor3.stop()
		GPIO.cleanup()

	def clamp(self, x, minimum=0, maximum=100):
		"""
		Clamps a PWM from 0-100 and puts it into the right servo usec timing.
		"""
		# minimum = 0
		# maximum = 100
		return 0 if x == 0 else max(minimum, min(x, maximum))

	def setMotors(self, m0, m1, m2, m3):
		"""
		Takes 4 tuples (shown below) for each motor.

		tuple: (dir, duty)

		MotorDriver.STOP    = 0
		MotorDriver.FORWARD = 1
		MotorDriver.REVERSE = 2
		MotorDriver.COAST   = 3
		"""
		# if not 'dir' in m0 or not 'duty' in m0: return
		# low = 0
		# high = 100

		# print(m0, m1, m2, m3)

		# set mux
		# val = m3['dir'] << 6 | m2['dir'] << 4 | m1['dir'] << 2 | m0['dir']
		# val = m3[0] << 6 | m2[0] << 4 | m1[0] << 2 | m0[0]
		# self.mux.write8(val)
		# GPIO.output(self.a0, m0[0])
		# GPIO.output(self.b0, m1[0])
		# GPIO.output(self.a1, m2[0])
		# GPIO.output(self.b1, m3[0])
		#
		# # set pwm
		# pwm = self.clamp(m0[1])
		# self.motor0.ChangeDutyCycle(pwm)
		#
		# pwm = self.clamp(m1[1])
		# self.motor1.ChangeDutyCycle(pwm)
		#
		# pwm = self.clamp(m2[1])
		# self.motor2.ChangeDutyCycle(pwm)
		#
		# pwm = self.clamp(m3[1])
		# self.motor3.ChangeDutyCycle(pwm)

		for pin, cmd, motor in zip(self.ctl, [m0, m1, m2, m3], [self.motor0, self.motor1, self.motor2, self.motor3]):
			GPIO.output(pin, cmd[0])
			pwm = self.clamp(cmd[1])
			motor.ChangeDutyCycle(pwm)

	def allStop(self):
		"""
		"""
		# self.mux.write8(0)
		# GPIO.output(self.a0, GPIO.LOW)
		# GPIO.output(self.b0, GPIO.LOW)
		# GPIO.output(self.a1, GPIO.LOW)
		# GPIO.output(self.a1, GPIO.LOW)
		for pin in self.ctl:
			GPIO.output(pin, GPIO.LOW)

		stop = (0, 0)
		self.setMotors(stop, stop, stop, stop)
