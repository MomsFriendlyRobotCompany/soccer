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
from sensors import AnalogIR, DigitalIR


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
		self.ir = DigitalIR([1, 2, 3, 4])
		self.air = AnalogIR()

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

	def run(self):
		cmd_sub = zmq.Sub(topics=['cmds'], connect_to=('0.0.0.0', 9000))
		telemetry_pub = zmq.Pub(bind_to=('0.0.0.0', 9010))

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
					cmd = self.makeCmd(msg)
					self.md.setMotors(*cmd)

			# get IR drop sensors
			ir_info = self.ir.read()
			msg = Msg.Range()
			msg.range = ir_info
			telemetry_pub.pub('ir', msg)
