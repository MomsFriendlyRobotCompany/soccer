#!/usr/bin/env python
# 7 Jan 2017

from __future__ import division
from __future__ import print_function
from multiprocessing import Process
from Soccer import SoccerRobot
from pygecko import ZmqClass as zmq
from pygecko import Messages as Msg
import time


def soccer():
	md_pins = [
		17, 18,  # m0 pwm a, b
		22, 23,  # m1 pwm a, b
		24, 25,  # m0 a, b
		26, 27   # m1 a, b
	]
	robot = SoccerRobot(md_pins)

	cmd_sub = zmq.Sub(topics=['cmds'], connect_to=('0.0.0.0', 9000))
	# telemetry_pub = zmq.Pub(bind_to=('0.0.0.0', 9010))

	while True:
		robot.loop_once()

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


def main():
	try:
		robot = Process(target=soccer).start()
	except KeyboardInterrupt:
		robot.join(0.1)
		if robot.is_alive():
			robot.terminate()

if __name__ == '__main__':
	main()
