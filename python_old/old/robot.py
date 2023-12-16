# #!/usr/bin/env python
#

from __future__ import division
from __future__ import print_function
from multiprocessing import Process


def soccer():
	pass


def main():
	try:
		robot = Process(target=soccer).start()
		robot.run()
	except KeyboardInterrupt:
		robot.join(0.1)
		if robot.is_alive():
			robot.terminate()

if __name__ == '__main__':
	main()
