#!/usr/bin/env python
#
# by Kevin J. Walchko
# 7 Jan 2017

from Soccer import SoccerHardware


if __name__ == '__main__':
	robot = SoccerHardware()
	# vision = VisionSystem()

	robot.start()
	# vision.start()  # not a process

	robot.join()
