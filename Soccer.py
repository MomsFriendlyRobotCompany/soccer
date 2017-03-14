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
import multiprocessing as mp
# import logging
import MotorDriver as md
from pygecko import ZmqClass as zmq
from pygecko import Messages as Msg
import platform
import os
if platform.system().lower() == 'linux' and 'CI' not in os.environ:
	from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	import RPi.GPIO as GPIO

else:
	from fakeHW import GPIO
	from fakeHW import MCP230XX


class DigitalIR(object):
	"""
	Read IR sensors on digital inputs

	Pololu sds01a 0-5 cm pwr 3V output max 3V
	Sharp xxx 0-15 cm pwr 5V output max 3V - digital gives 3 inch range
	"""
	def __init__(self, pins):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		for p in pins: GPIO.setup(p, GPIO.IN)
		self.pins = pins

	def read(self):
		ir = []
		for p in self.pins: ir.append(GPIO.input(p))
		return ir


class SoccerHardware(mp.Process):
	"""
	RobotHardwareServer handles incoming commands streamed from somewhere else.
	in: commands/etc
	out: sensor readings
	"""
	def __init__(self):
		mp.Process.__init__(self)
		# logging.basicConfig(level=logging.INFO)
		# self.logger = logging.getLogger('robot')
		self.md = md.MotorDriver(17, 18, 22, 23)
		self.ir = DigitalIR([1, 2, 3])

	def __del__(self):
		self.md.allStop()

	def shutdown(self):
		"""
		Needed?
		"""
		pass

	# def test(self):
	# 	dt = 5
	# 	go = {'dir': md.MotorDriver.FORWARD, 'duty': 10}
	# 	rev = {'dir': md.MotorDriver.REVERSE, 'duty': 10}
	# 	stp = {'dir': md.MotorDriver.REVERSE, 'duty': 10}
	#
	# 	self.md.setMotors(go, go, go, go)
	# 	time.sleep(dt)
	# 	self.md.setMotors(rev, rev, rev, rev)
	# 	time.sleep(dt)
	# 	self.md.setMotors(go, stp, go, stp)
	# 	time.sleep(dt)
	# 	self.md.setMotors(stp, rev, stp, rev)
	# 	time.sleep(dt)
	# 	self.md.allStop()

	def run(self):
		cmd_sub = zmq.Sub(topics=['cmds'], connect_to=('0.0.0.0', 9000))
		telemetry_pub = zmq.Pub(bind_to=('0.0.0.0', 9010))

		cmd = {'dir': 0, 'duty': 0}

		while True:
			time.sleep(0.05)  # 0.5 => 20Hz

			# get info
			topic, msg = cmd_sub.recv()
			if msg:
				print('msg:', topic, msg)

				if topic == 'quit':
					self.shutdown()
					break
				elif topic == 'cmd':
					# need logic for command
					self.md.setMotors(cmd)

			# get IR drop sensors
			ir_info = self.ir.read()
			msg = Msg.Range()
			msg.range = ir_info
			telemetry_pub.pub('ir', msg)
