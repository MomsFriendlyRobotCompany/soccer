#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# Log:
# 12 Oct 14 Broke out into its own file
#
from __future__ import division
from __future__ import print_function
import time
# import multiprocessing as mp
# import logging
from Hardware import AnalogIR, DigitalIR
# from pygecko import Messages as Msg
import Hardware as md
import os
import platform

try:
	if 'CI' in os.environ or platform.system() != 'Linux':
		raise ImportError()

	from nxp_imu import IMU, AHRS

except ImportError:
	from fake_rpi.nxp_imu import IMU, AHRS


class SoccerRobot(object):
	"""
	This is the low level robot hardware driver:
	- motor driver x2
	- ADC (8 ch): IR
	"""
	def __init__(self, md_pins):
		# mp.Process.__init__(self)
		# logging.basicConfig(level=logging.INFO)
		# self.logger = logging.getLogger('robot')
		if len(md_pins) != 8:
			raise Exception('Wrong number of pins for motor driver!')

		self.md = md.MotorDriver(*md_pins)
		self.digital_ir = DigitalIR([1, 2, 3, 4])
		self.analog_ir = AnalogIR()
		self.imu = IMU()
		self.ahrs = AHRS(True)

	def __del__(self):
		self.md.allStop()

	def shutdown(self):
		"""
		Needed?
		"""
		pass

	def makeCmd(self, msg):
		# msg should be a twist FIXME
		m0 = m1 = m2 = m3 = (0, 0)
		return m0, m1, m2, m3

	def loop_once(self):

		while True:
			# get sensors
			self.analog_ir.read()
			ret = self.imu.get()
			self.accel = ret[:3]
			self.mag = ret[3:6]
			self.gyro = ret[6:]
			self.orientation = self.ahrs.getOrientation(self.accel, self.mag)

			time.sleep(0.05)  # 0.05 => 20Hz
