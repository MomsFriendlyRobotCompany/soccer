#!/usr/bin/env python
from __future__ import absolute_import
from ..MotorDriver import MotorDriver


def test():
	md = MotorDriver(1, 2, 3, 4, 5, 6, 7, 8)
	assert md.clamp(101.0) == 100.0 and md.clamp(-0.01) == 0.0
