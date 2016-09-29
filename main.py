#!/usr/bin/python

import sensor

pin = [17, 4, 11, 18]
while True:
	if sensor.detect_motion(pin) is True:
		print('motion detected')

		
