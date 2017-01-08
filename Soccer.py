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
from pygecko.lib import ZmqClass as zmq
from pygecko.lib import Messages as Msg
# import lib.FileStorage as Fs


import platform
import os
if platform.system().lower() == 'linux' and 'CI' not in os.environ:
	# from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	import RPi.GPIO as GPIO

else:
	from fakeHW import GPIO


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


class SoccerHardwareServer(mp.Process):
	"""
	RobotHardwareServer handles incoming commands streamed from somewhere else.
	in: commands/etc
	out: sensor readings
	"""
	def __init__(self):
		mp.Process.__init__(self)
		# self.port = port
		# logging.basicConfig(level=logging.INFO)
		# self.logger = logging.getLogger('robot')
		self.md = md.MotorDriver(17, 18, 22, 23)
		self.ir = DigitalIR([1, 2, 3])

	def createMotorCmd(self, dir, duty):
		return {'dir': dir, 'duty': duty}

	def soundCmd(self, cmd):
		# self.logger.info(cmd)
		pass

	def parseMsg(self, msg):
		if 'quit' in msg:
			self.shutdown()
		elif 'cmd' in msg:
			cmd = msg['cmd']
			if 'm' in cmd:
				self.motorCmd(cmd)
			elif 's' in cmd:
				self.soundCmd(cmd)

	def __del__(self):
		self.md.allStop()

	def on_message(self, client, userdata, msg):
		print(msg.topic + ' ' + str(msg.payload))

	def shutdown(self):
		"""
		Needed?
		"""
		pass

	def test(self):
		dt = 5
		go = {'dir': md.MotorDriver.FORWARD, 'duty': 10}
		rev = {'dir': md.MotorDriver.REVERSE, 'duty': 10}
		stp = {'dir': md.MotorDriver.REVERSE, 'duty': 10}

		self.md.setMotors(go, go, go, go)
		time.sleep(dt)
		self.md.setMotors(rev, rev, rev, rev)
		time.sleep(dt)
		self.md.setMotors(go, stp, go, stp)
		time.sleep(dt)
		self.md.setMotors(stp, rev, stp, rev)
		time.sleep(dt)
		self.md.allStop()

	def run(self):
		# self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on' +
		# 	str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))
		# p = Publisher((self.host,self.port))
		# self.pub = p.accept()
		# self.logger.info('Accepted connection: ')

		self.sub = zmq.Sub(topics=['cmds'], connect_to=('0.0.0.0', 9000))
		self.pub = zmq.Pub(bind_to=('0.0.0.0', 9010))

		while True:
			time.sleep(0.05)  # 0.5 => 20Hz
			# get info
			# topic, msg = self.sub.recv()
			# if msg:
			# 	print('msg:', topic, msg)
# 				self.parseMsg( msg )
			# get IR sensors
			ir_info = self.ir.read()
			ir = Msg.Range()
			self.pub.pub('ir', ir)
			# get drop sensors
			# send motor commands
			# send head servo commands
			self.test()


# class NonHolonomic(RobotHardwareServer):
# 	def __init__(self, host="localhost", port=9000):
# 		RobotHardwareServer.__init__(self, host, port)
# 		# self.md = md.MotorDriver(11, 12)  # FIXME: 20160528 why these two pins?
# 		# self.md.allStop()
#
# 	def motorCmd(self, cmd):
# 		self.logger.info(cmd)
# 		# self.md.setMotors(cmd)
#
#
# class Holonomic(RobotHardwareServer):
# 	def __init__(self, host="localhost", port=9000, pinA=11, pinB=12, pinC=15, pinD=16):
# 		RobotHardwareServer.__init__(self, host, port)
# 		self.md = md.MotorDriver(pinA, pinB, pinC, pinD)
# 		self.md.allStop()
#
# 	def motorCmd(self, cmd):
# 		self.logger.info(cmd)
# 		# self.md.setMotors(cmd)

#
# if __name__ == '__main__':
# 	c = Holonomic()
# 	c.run()
